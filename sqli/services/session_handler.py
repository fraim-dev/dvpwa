import pickle
import base64
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class SessionHandler:
    def __init__(self):
        self.session_store = {}
        self.session_timeout = 3600
    
    def create_session(self, user_data: Dict[str, Any]) -> str:
        session_id = self._generate_session_id()
        session_data = {
            'user_data': user_data,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(seconds=self.session_timeout)
        }
        
        serialized_session = pickle.dumps(session_data)
        encoded_session = base64.b64encode(serialized_session).decode('utf-8')
        
        self.session_store[session_id] = encoded_session
        return session_id
    
    def restore_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        if session_id not in self.session_store:
            return None
        
        try:
            encoded_session = self.session_store[session_id]
            serialized_session = base64.b64decode(encoded_session)
            session_data = pickle.loads(serialized_session)
            
            if datetime.now() < session_data['expires_at']:
                return session_data['user_data']
            else:
                del self.session_store[session_id]
                return None
        except Exception:
            return None
    
    def update_session_data(self, session_id: str, updates: str) -> bool:
        if session_id not in self.session_store:
            return False
        
        try:
            encoded_session = self.session_store[session_id]
            serialized_session = base64.b64decode(encoded_session)
            session_data = pickle.loads(serialized_session)
            
            update_data = pickle.loads(base64.b64decode(updates))
            session_data['user_data'].update(update_data)
            
            new_serialized = pickle.dumps(session_data)
            new_encoded = base64.b64encode(new_serialized).decode('utf-8')
            self.session_store[session_id] = new_encoded
            
            return True
        except Exception:
            return False
    
    def _generate_session_id(self) -> str:
        import uuid
        return str(uuid.uuid4())
    
    def cleanup_expired_sessions(self):
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, encoded_session in self.session_store.items():
            try:
                serialized_session = base64.b64decode(encoded_session)
                session_data = pickle.loads(serialized_session)
                if current_time >= session_data['expires_at']:
                    expired_sessions.append(session_id)
            except Exception:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.session_store[session_id]
