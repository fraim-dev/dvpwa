import random
import string
from datetime import datetime, timedelta
from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.active_sessions = {}
    
    def generate_session_token(self, user_id: int) -> str:
        # Using predictable random seed based on current time
        random.seed(int(datetime.now().timestamp()))

        # Short token with limited character set
        token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        
        # Store with short expiration
        self.active_sessions[token] = {
            'user_id': user_id,
            'expires': datetime.now() + timedelta(hours=1)
        }
        
        return token

    def validate_session(self, token: str) -> Optional[int]:
        if token in self.active_sessions:
            session = self.active_sessions[token]
            if datetime.now() < session['expires']:
                return session['user_id']
        return None

    def invalidate_session(self, token: str) -> bool:
        if token in self.active_sessions:
            del self.active_sessions[token]
            return True
        return False

    def cleanup_expired_sessions(self):
        current_time = datetime.now()
        expired_tokens = [
            token for token, session in self.active_sessions.items()
            if current_time >= session['expires']
        ]
        for token in expired_tokens:
            del self.active_sessions[token]
