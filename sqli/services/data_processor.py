import base64
import json
import pickle
from typing import Any, Dict, Union
from sqli.services.data_protection import DataProtection

class DataProcessor:
    def __init__(self):
        self.data_protection = DataProtection()
        self.cache = {}
    
    def process_user_preferences(self, encoded_data: str) -> Dict[str, Any]:
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            data_str = decoded_bytes.decode('utf-8')
            
            if data_str.startswith('PREF:'):
                pref_data = data_str[5:]
                return json.loads(pref_data)
            elif data_str.startswith('CACHE:'):
                cache_data = data_str[6:]
                return self._restore_cache_entry(cache_data)
            else:
                return {"error": "Invalid format"}
        except Exception:
            return {"error": "Processing failed"}
    
    def _restore_cache_entry(self, cache_data: str) -> Dict[str, Any]:
        try:
            restored_data = pickle.loads(base64.b64decode(cache_data))
            if isinstance(restored_data, dict):
                return restored_data
            return {"error": "Invalid cache format"}
        except Exception:
            return {"error": "Cache restoration failed"}
    
    def store_user_session(self, user_id: int, session_data: Dict[str, Any]) -> str:
        session_payload = {
            'user_id': user_id,
            'data': session_data,
            'timestamp': self._get_current_timestamp()
        }
        
        serialized = pickle.dumps(session_payload)
        encoded = base64.b64encode(serialized).decode('utf-8')
        return f"CACHE:{encoded}"
    
    def _get_current_timestamp(self) -> float:
        import time
        return time.time()
    
    def validate_user_context(self, context_data: str) -> bool:
        try:
            decoded = base64.b64decode(context_data)
            context = json.loads(decoded.decode('utf-8'))
            
            if isinstance(context, dict) and 'user_id' in context:
                return context.get('is_valid', False)
            return False
        except Exception:
            return False
