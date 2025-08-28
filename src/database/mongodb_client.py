"""
MongoDB Client for Interview Topics
Handles database operations for storing generated interview topics
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import asyncio

try:
    from motor.motor_asyncio import AsyncIOMotorClient
    from pymongo.errors import DuplicateKeyError, ConnectionFailure
    import pymongo
except ImportError as e:
    raise ImportError(f"Required MongoDB libraries not installed: {e}")

logger = logging.getLogger(__name__)


class MongoDBClient:
    """Async MongoDB client for interview topics storage"""
    
    def __init__(self, connection_uri: str, database_name: str = "interview_topics"):
        self.connection_uri = connection_uri
        self.database_name = database_name
        self.collection_name = "topics"
        
        self.client = None
        self.database = None
        self.collection = None
        self.connected = False
    
    async def connect(self):
        """Establish connection to MongoDB"""
        try:
            logger.info("🔌 Connecting to MongoDB...")
            
            # Create async MongoDB client
            self.client = AsyncIOMotorClient(
                self.connection_uri,
                serverSelectionTimeoutMS=10000,  # 10 second timeout
                connectTimeoutMS=10000,
                socketTimeoutMS=10000,
                maxPoolSize=10,
                minPoolSize=1
            )
            
            # Test connection
            await self.client.admin.command('ping')
            
            # Get database and collection references
            self.database = self.client[self.database_name]
            self.collection = self.database[self.collection_name]
            
            # Ensure indexes
            await self._ensure_indexes()
            
            self.connected = True
            logger.info(f"✅ Connected to MongoDB database: {self.database_name}")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            raise ConnectionFailure(f"MongoDB connection failed: {e}")
    
    async def _ensure_indexes(self):
        """Create necessary indexes for optimal performance"""
        try:
            # Index on runId for fast lookups
            await self.collection.create_index([("runId", pymongo.ASCENDING)], unique=True)
            
            # Index on generatedAt for time-based queries
            await self.collection.create_index([("generatedAt", pymongo.DESCENDING)])
            
            # Compound index on topic fields for searching
            await self.collection.create_index([
                ("topics.category", pymongo.ASCENDING),
                ("topics.difficulty", pymongo.ASCENDING)
            ])
            
            # Text index for topic title and description search
            await self.collection.create_index([
                ("topics.title", "text"),
                ("topics.description", "text")
            ])
            
            logger.info("✅ MongoDB indexes ensured")
            
        except Exception as e:
            logger.warning(f"⚠️ Could not create indexes: {e}")
    
    async def insert_topics_document(self, document: Dict[str, Any]) -> str:
        """Insert a complete topics document"""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            # Validate document structure
            self._validate_document(document)
            
            # Add metadata
            document['_metadata'] = {
                'insertedAt': datetime.now(timezone.utc),
                'version': '1.0.0',
                'source': 'github-adk-agent'
            }
            
            # Insert document
            result = await self.collection.insert_one(document)
            
            logger.info(f"✅ Inserted document with {len(document.get('topics', []))} topics")
            return str(result.inserted_id)
            
        except DuplicateKeyError:
            logger.error(f"❌ Document with runId '{document.get('runId')}' already exists")
            raise ValueError(f"Run ID already exists: {document.get('runId')}")
        except Exception as e:
            logger.error(f"❌ Failed to insert document: {e}")
            raise
    
    def _validate_document(self, document: Dict[str, Any]):
        """Validate document structure before insertion"""
        required_fields = ['runId', 'generatedAt', 'model', 'topics']
        
        for field in required_fields:
            if field not in document:
                raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(document['topics'], list):
            raise ValueError("Topics must be a list")
        
        if len(document['topics']) == 0:
            raise ValueError("Topics list cannot be empty")
        
        # Validate topic structure
        topic_required_fields = ['title', 'category', 'difficulty', 'description']
        
        for i, topic in enumerate(document['topics']):
            for field in topic_required_fields:
                if field not in topic:
                    raise ValueError(f"Topic {i+1} missing required field: {field}")
    
    async def get_topics_by_run_id(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve topics document by run ID"""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            document = await self.collection.find_one({"runId": run_id})
            return document
        except Exception as e:
            logger.error(f"❌ Failed to retrieve document: {e}")
            raise
    
    async def get_recent_topics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent topic documents"""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            cursor = self.collection.find().sort("generatedAt", -1).limit(limit)
            documents = await cursor.to_list(length=limit)
            return documents
        except Exception as e:
            logger.error(f"❌ Failed to retrieve recent topics: {e}")
            raise
    
    async def search_topics(
        self, 
        category: Optional[str] = None,
        difficulty: Optional[str] = None,
        text_search: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Search topics with various filters"""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            # Build query
            query = {}
            
            if category:
                query["topics.category"] = category
            
            if difficulty:
                query["topics.difficulty"] = difficulty
            
            if text_search:
                query["$text"] = {"$search": text_search}
            
            # Execute query
            cursor = self.collection.find(query).sort("generatedAt", -1).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return documents
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.connected:
            raise ConnectionError("Not connected to MongoDB")
        
        try:
            # Total documents
            total_documents = await self.collection.count_documents({})
            
            # Total topics across all documents
            pipeline = [
                {"$project": {"topicCount": {"$size": "$topics"}}},
                {"$group": {"_id": None, "totalTopics": {"$sum": "$topicCount"}}}
            ]
            
            result = await self.collection.aggregate(pipeline).to_list(length=1)
            total_topics = result[0]["totalTopics"] if result else 0
            
            # Most recent generation
            recent = await self.collection.find().sort("generatedAt", -1).limit(1).to_list(length=1)
            last_generation = recent[0]["generatedAt"] if recent else None
            
            # Categories distribution
            pipeline = [
                {"$unwind": "$topics"},
                {"$group": {"_id": "$topics.category", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            
            categories = await self.collection.aggregate(pipeline).to_list(length=None)
            
            # Difficulties distribution
            pipeline = [
                {"$unwind": "$topics"},
                {"$group": {"_id": "$topics.difficulty", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]
            
            difficulties = await self.collection.aggregate(pipeline).to_list(length=None)
            
            return {
                "totalDocuments": total_documents,
                "totalTopics": total_topics,
                "lastGeneration": last_generation,
                "categoriesDistribution": {cat["_id"]: cat["count"] for cat in categories},
                "difficultiesDistribution": {diff["_id"]: diff["count"] for diff in difficulties}
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            raise
    
    async def close(self):
        """Close the MongoDB connection"""
        try:
            if self.client:
                self.client.close()
                self.connected = False
                logger.info("✅ MongoDB connection closed")
        except Exception as e:
            logger.warning(f"⚠️ Error closing MongoDB connection: {e}")


# Utility functions for testing
async def test_connection(connection_uri: str) -> bool:
    """Test MongoDB connection"""
    client = MongoDBClient(connection_uri)
    try:
        await client.connect()
        stats = await client.get_stats()
        logger.info(f"📊 Database stats: {stats}")
        return True
    except Exception as e:
        logger.error(f"❌ Connection test failed: {e}")
        return False
    finally:
        await client.close()


if __name__ == "__main__":
    # Simple connection test
    import os
    import sys
    
    uri = os.getenv("MONGODB_URI")
    if not uri:
        print("❌ MONGODB_URI environment variable not set")
        sys.exit(1)
    
    async def main():
        success = await test_connection(uri)
        if success:
            print("✅ MongoDB connection test passed")
        else:
            print("❌ MongoDB connection test failed")
            sys.exit(1)
    
    asyncio.run(main())