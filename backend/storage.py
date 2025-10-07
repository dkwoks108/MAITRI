"""
Google Drive Storage Module
Handles saving and retrieving session data from Google Drive
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import os

logger = logging.getLogger(__name__)

class GoogleDriveStorage:
    """Handles Google Drive storage operations"""
    
    def __init__(self):
        """Initialize Google Drive client"""
        self.service = None
        self.folder_id = None
        self._init_drive()
        
    def _init_drive(self):
        """Initialize Google Drive API connection"""
        try:
            # Try to import Google Drive API
            try:
                from googleapiclient.discovery import build
                from google.oauth2 import service_account
                
                # Check for credentials file
                creds_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
                
                if os.path.exists(creds_path):
                    SCOPES = ['https://www.googleapis.com/auth/drive.file']
                    credentials = service_account.Credentials.from_service_account_file(
                        creds_path, scopes=SCOPES
                    )
                    self.service = build('drive', 'v3', credentials=credentials)
                    logger.info("Google Drive API initialized successfully")
                    
                    # Get or create MAITRI_Data folder
                    self._setup_folders()
                else:
                    logger.warning("Google credentials not found, using local storage fallback")
                    self.service = None
                    
            except ImportError:
                logger.warning("Google API client not available, using local storage")
                self.service = None
                
        except Exception as e:
            logger.error(f"Error initializing Google Drive: {e}")
            self.service = None
    
    def _setup_folders(self):
        """Create MAITRI folder structure on Google Drive"""
        try:
            if self.service is None:
                return
                
            # Search for MAITRI_Data folder
            query = "name='MAITRI_Data' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)'
            ).execute()
            
            files = results.get('files', [])
            
            if files:
                self.folder_id = files[0]['id']
                logger.info(f"Found MAITRI_Data folder: {self.folder_id}")
            else:
                # Create folder
                folder_metadata = {
                    'name': 'MAITRI_Data',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                self.folder_id = folder.get('id')
                logger.info(f"Created MAITRI_Data folder: {self.folder_id}")
                
        except Exception as e:
            logger.error(f"Error setting up folders: {e}")
    
    def save_session(self, session_data: Dict, user_id: str) -> str:
        """
        Save session data to Google Drive or local storage
        
        Args:
            session_data: Session information to save
            user_id: User identifier
            
        Returns:
            File ID or path
        """
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{user_id}_{timestamp}.json"
            
            # Convert to JSON
            json_data = json.dumps(session_data, indent=2)
            
            if self.service is not None and self.folder_id is not None:
                # Save to Google Drive
                return self._save_to_drive(filename, json_data)
            else:
                # Save locally as fallback
                return self._save_locally(filename, json_data)
                
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            # Try local fallback
            return self._save_locally(filename, json_data)
    
    def _save_to_drive(self, filename: str, json_data: str) -> str:
        """Save file to Google Drive"""
        try:
            from googleapiclient.http import MediaInMemoryUpload
            
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            media = MediaInMemoryUpload(
                json_data.encode('utf-8'),
                mimetype='application/json',
                resumable=True
            )
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            logger.info(f"Saved to Google Drive: {file_id}")
            return file_id
            
        except Exception as e:
            logger.error(f"Error saving to Drive: {e}")
            raise
    
    def _save_locally(self, filename: str, json_data: str) -> str:
        """Save file locally as fallback"""
        try:
            # Create local data directory
            data_dir = "data/sessions"
            os.makedirs(data_dir, exist_ok=True)
            
            filepath = os.path.join(data_dir, filename)
            
            with open(filepath, 'w') as f:
                f.write(json_data)
            
            logger.info(f"Saved locally: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving locally: {e}")
            raise
    
    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        Retrieve recent sessions for a user
        
        Args:
            user_id: User identifier
            limit: Maximum number of sessions to retrieve
            
        Returns:
            List of session data dictionaries
        """
        try:
            if self.service is not None and self.folder_id is not None:
                return self._get_from_drive(user_id, limit)
            else:
                return self._get_locally(user_id, limit)
                
        except Exception as e:
            logger.error(f"Error retrieving sessions: {e}")
            return []
    
    def _get_from_drive(self, user_id: str, limit: int) -> List[Dict]:
        """Retrieve sessions from Google Drive"""
        try:
            # Search for user's session files
            query = f"name contains 'session_{user_id}' and '{self.folder_id}' in parents"
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, createdTime)',
                orderBy='createdTime desc',
                pageSize=limit
            ).execute()
            
            files = results.get('files', [])
            sessions = []
            
            for file in files:
                # Download file content
                content = self.service.files().get_media(fileId=file['id']).execute()
                session_data = json.loads(content.decode('utf-8'))
                sessions.append(session_data)
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting from Drive: {e}")
            return []
    
    def _get_locally(self, user_id: str, limit: int) -> List[Dict]:
        """Retrieve sessions from local storage"""
        try:
            data_dir = "data/sessions"
            
            if not os.path.exists(data_dir):
                return []
            
            # Get all session files for user
            files = [f for f in os.listdir(data_dir) 
                    if f.startswith(f"session_{user_id}") and f.endswith('.json')]
            
            # Sort by modification time (newest first)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(data_dir, x)), 
                      reverse=True)
            
            # Load the files
            sessions = []
            for filename in files[:limit]:
                filepath = os.path.join(data_dir, filename)
                with open(filepath, 'r') as f:
                    session_data = json.load(f)
                    sessions.append(session_data)
            
            return sessions
            
        except Exception as e:
            logger.error(f"Error getting locally: {e}")
            return []
