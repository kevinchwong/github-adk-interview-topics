"""
Firebase Firestore Client for Interview Topics
Handles database operations for storing generated interview topics in Firestore
"""

import logging
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
except ImportError as e:
    raise ImportError(f"Required Firebase libraries not installed: {e}")

logger = logging.getLogger(__name__)


class FirebaseClient:
    """Firebase Firestore client for interview topics storage"""
    
    def __init__(self, project_id: str, credentials_json: Optional[str] = None):
        self.project_id = project_id
        self.credentials_json = credentials_json
        self.collection_name = "topics"
        
        # Check for GOOGLE_APPLICATION_CREDENTIALS as fallback
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        self.app = None
        self.db = None
        self.collection = None
        self.connected = False
    
    async def connect(self):
        """Establish connection to Firestore"""
        try:
            logger.info("🔌 Connecting to Firebase Firestore...")
            
            # Initialize Firebase app if not already done
            if not firebase_admin._apps:
                if self.credentials_path and os.path.exists(self.credentials_path):
                    # Use credentials file path
                    cred = credentials.Certificate(self.credentials_path)
                    self.app = firebase_admin.initialize_app(cred, {
                        'projectId': self.project_id
                    })
                    logger.info(f"✅ Using Firebase credentials from: {self.credentials_path}")
                elif self.credentials_json:
                    try:
                        # Use provided credentials JSON
                        cred_dict = json.loads(self.credentials_json)
                        cred = credentials.Certificate(cred_dict)
                        self.app = firebase_admin.initialize_app(cred, {
                            'projectId': self.project_id
                        })
                        logger.info("✅ Using Firebase credentials from JSON")
                    except json.JSONDecodeError:
                        # Fall back to default credentials if JSON parsing fails
                        logger.warning("⚠️ Failed to parse Firebase credentials JSON, using default credentials")
                        self.app = firebase_admin.initialize_app()
                else:
                    # Use default credentials (for local development)
                    logger.info("✅ Using default Firebase credentials")
                    self.app = firebase_admin.initialize_app()
            else:
                self.app = firebase_admin.get_app()
            
            # Get Firestore client
            self.db = firestore.client(app=self.app)
            self.collection = self.db.collection(self.collection_name)
            
            # Test connection by performing a simple query
            try:
                await self._test_connection()
            except Exception as e:
                logger.warning(f"⚠️ Firestore connection test failed (but proceeding): {e}")
            
            self.connected = True
            logger.info(f"✅ Connected to Firestore database: {self.project_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to connect to Firestore: {e}")
            raise ConnectionError(f"Firebase connection failed: {e}")
    
    async def _test_connection(self):
        """Test Firestore connection"""
        try:
            # Simple test query
            docs = self.collection.limit(1).get()
            logger.debug("✅ Firestore connection test passed")
        except Exception as e:
            raise ConnectionError(f"Firestore connection test failed: {e}")
    
    async def insert_topics_document(self, document: Dict[str, Any]) -> str:
        """Insert a complete topics document"""
        if not self.connected:
            raise ConnectionError("Not connected to Firestore")
        
        try:
            # Validate document structure
            self._validate_document(document)
            
            # Add metadata
            document['_metadata'] = {
                'insertedAt': datetime.now(timezone.utc),
                'version': '1.0.0',
                'source': 'github-adk-agent'
            }
            
            # Use runId as document ID to prevent duplicates
            doc_id = document['runId']
            doc_ref = self.collection.document(doc_id)
            
            # Check if document already exists
            if doc_ref.get().exists:
                logger.error(f"❌ Document with runId '{doc_id}' already exists")
                raise ValueError(f"Run ID already exists: {doc_id}")
            
            # Insert document
            doc_ref.set(document)
            
            logger.info(f"✅ Inserted document with {len(document.get('topics', []))} topics")
            return doc_id
            
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
            raise ConnectionError("Not connected to Firestore")
        
        try:
            doc_ref = self.collection.document(run_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"❌ Failed to retrieve document: {e}")
            raise
    
    async def get_recent_topics(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent topic documents"""
        if not self.connected:
            raise ConnectionError("Not connected to Firestore")
        
        try:
            docs = (self.collection
                   .order_by('generatedAt', direction=firestore.Query.DESCENDING)
                   .limit(limit)
                   .get())
            
            return [doc.to_dict() for doc in docs]
            
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
            raise ConnectionError("Not connected to Firestore")
        
        try:
            query = self.collection
            
            if category:
                query = query.where(filter=FieldFilter("topics", "array_contains", {"category": category}))
            
            if difficulty:
                query = query.where(filter=FieldFilter("topics", "array_contains", {"difficulty": difficulty}))
            
            # Note: Firestore doesn't have full-text search like MongoDB
            # For text search, you'd need to implement a different approach
            
            docs = query.limit(limit).get()
            return [doc.to_dict() for doc in docs]
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.connected:
            raise ConnectionError("Not connected to Firestore")
        
        try:
            # Get all documents for stats
            docs = list(self.collection.get())
            total_documents = len(docs)
            
            if total_documents == 0:
                return {
                    "totalDocuments": 0,
                    "totalTopics": 0,
                    "lastGeneration": None,
                    "categoriesDistribution": {},
                    "difficultiesDistribution": {}
                }
            
            # Calculate statistics
            total_topics = 0
            categories = {}
            difficulties = {}
            last_generation = None
            
            for doc in docs:
                data = doc.to_dict()
                topics = data.get('topics', [])
                total_topics += len(topics)
                
                # Track most recent generation
                gen_date = data.get('generatedAt')
                if not last_generation or (gen_date and gen_date > last_generation):
                    last_generation = gen_date
                
                # Count categories and difficulties
                for topic in topics:
                    cat = topic.get('category', 'unknown')
                    diff = topic.get('difficulty', 'unknown')
                    categories[cat] = categories.get(cat, 0) + 1
                    difficulties[diff] = difficulties.get(diff, 0) + 1
            
            return {
                "totalDocuments": total_documents,
                "totalTopics": total_topics,
                "lastGeneration": last_generation,
                "categoriesDistribution": categories,
                "difficultiesDistribution": difficulties
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get stats: {e}")
            raise
    
    async def close(self):
        """Close the Firebase connection"""
        try:
            if self.app:
                firebase_admin.delete_app(self.app)
                self.connected = False
                logger.info("✅ Firebase connection closed")
        except Exception as e:
            logger.warning(f"⚠️ Error closing Firebase connection: {e}")


# Utility functions for testing
async def test_connection(project_id: str, credentials_json: Optional[str] = None) -> bool:
    """Test Firebase connection"""
    client = FirebaseClient(project_id, credentials_json)
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
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
    
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT environment variable not set")
        sys.exit(1)
    
    async def main():
        success = await test_connection(project_id, credentials_json)
        if success:
            print("✅ Firebase connection test passed")
        else:
            print("❌ Firebase connection test failed")
            sys.exit(1)
    
    asyncio.run(main())