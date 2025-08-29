"""
Google Cloud Firestore Client Factory for Interview Topics
"""

import logging
import os
from typing import Dict

logger = logging.getLogger(__name__)


class DatabaseFactory:
    """Factory class for creating Google Cloud Firestore client"""
    
    @staticmethod
    def create_client():
        """Create Google Cloud Firestore client"""
        try:
            from .firebase_client import FirebaseClient
        except ImportError as e:
            raise ImportError(f"Google Cloud Firestore dependencies not available: {e}")
            
        google_cloud_project = os.getenv("GOOGLE_CLOUD_PROJECT")
        if not google_cloud_project:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
        
        firestore_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        
        logger.info("🔧 Creating Google Cloud Firestore client")
        return FirebaseClient(google_cloud_project, firestore_credentials)
    
    @staticmethod
    def get_provider_name() -> str:
        """Get the current database provider name"""
        return "FIRESTORE"
    
    @staticmethod
    def validate_provider_config() -> Dict[str, str]:
        """Validate Firebase configuration"""
        required_vars = {
            'GOOGLE_CLOUD_PROJECT': 'Firebase project ID'
        }
        
        env_vars = {}
        missing_vars = []
        
        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                missing_vars.append(f"{var} ({description})")
            else:
                env_vars[var] = value
        
        if missing_vars:
            logger.error("Missing required environment variables for Firebase:")
            for var in missing_vars:
                logger.error(f"  - {var}")
            raise ValueError("Required Firebase environment variables not set")
        
        return env_vars