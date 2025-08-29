"""
Database Factory for Interview Topics
Handles switching between MongoDB and Firebase based on configuration
"""

import logging
import os
from typing import Union, Dict

logger = logging.getLogger(__name__)


class DatabaseFactory:
    """Factory class for creating database clients based on provider configuration"""
    
    @staticmethod
    def create_client():
        """Create appropriate database client based on DATABASE_PROVIDER environment variable"""
        
        provider = os.getenv("DATABASE_PROVIDER", "MONGO").upper()
        
        logger.info(f"🔧 [create_client] Creating database client for provider: {provider}")
        
        if provider == "MONGO":
            return DatabaseFactory._create_mongodb_client()
        elif provider == "FIREBASE":
            return DatabaseFactory._create_firebase_client()
        else:
            raise ValueError(f"Unsupported database provider: {provider}. Supported: MONGO, FIREBASE")
    
    @staticmethod
    def _create_mongodb_client():
        """Create MongoDB client"""
        try:
            from .mongodb_client import MongoDBClient
        except ImportError as e:
            raise ImportError(f"MongoDB dependencies not available: {e}")
            
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required for MongoDB provider")
        
        logger.info("🔧 Creating MongoDB client")
        return MongoDBClient(mongodb_uri)
    
    @staticmethod
    def _create_firebase_client():
        """Create Firebase client"""
        try:
            from .firebase_client import FirebaseClient
        except ImportError as e:
            raise ImportError(f"Firebase dependencies not available: {e}")
            
        GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not GOOGLE_CLOUD_PROJECT:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required for Firebase provider")
        
        firebase_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        logger.info("🔧 Creating Firebase client")
        return FirebaseClient(GOOGLE_CLOUD_PROJECT, firebase_credentials)
    
    @staticmethod
    def get_provider_name() -> str:
        """Get the current database provider name"""
        return os.getenv("DATABASE_PROVIDER", "MONGO").upper()
    
    @staticmethod
    def validate_provider_config() -> Dict[str, str]:
        """Validate configuration for the selected provider"""
        provider = DatabaseFactory.get_provider_name()
        
        if provider == "MONGO":
            required_vars = {
                'MONGODB_URI': 'MongoDB connection string'
            }
        elif provider == "FIREBASE":
            required_vars = {
                'GOOGLE_CLOUD_PROJECT': 'Firebase project ID'
            }
            # GOOGLE_APPLICATION_CREDENTIALS_JSON is optional (can use default auth)
        else:
            raise ValueError(f"Unsupported database provider: {provider}")
        
        env_vars = {}
        missing_vars = []
        
        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                missing_vars.append(f"{var} ({description})")
            else:
                env_vars[var] = value
        
        if missing_vars:
            logger.error(f"Missing required environment variables for {provider}:")
            for var in missing_vars:
                logger.error(f"  - {var}")
            raise ValueError(f"Required {provider} environment variables not set")
        
        return env_vars