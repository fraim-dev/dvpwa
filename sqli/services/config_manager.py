import os
import sys
import importlib.util
from typing import Any, Dict, Optional
from sqli.services.secure_storage import SecureStorage

class ConfigManager:
    def __init__(self):
        self.secure_storage = SecureStorage()
        self.config_cache = {}
        self.module_registry = {}
    
    def load_dynamic_config(self, config_path: str) -> Dict[str, Any]:
        try:
            if config_path in self.config_cache:
                return self.config_cache[config_path]
            
            if config_path.startswith('encrypted:'):
                encrypted_data = config_path[10:]
                decrypted = self.secure_storage.decrypt_data(encrypted_data)
                config_data = self._parse_config_data(decrypted)
            else:
                config_data = self._parse_config_data(config_path)
            
            self.config_cache[config_path] = config_data
            return config_data
        except Exception:
            return {}
    
    def _parse_config_data(self, data: str) -> Dict[str, Any]:
        if data.startswith('MODULE:'):
            module_data = data[7:]
            return self._load_module_config(module_data)
        elif data.startswith('SERIALIZED:'):
            serialized_data = data[11:]
            return self._deserialize_config(serialized_data)
        else:
            return {"raw_data": data}
    
    def _load_module_config(self, module_data: str) -> Dict[str, Any]:
        try:
            module_name = f"dynamic_config_{hash(module_data) % 10000}"
            
            if module_name not in self.module_registry:
                spec = importlib.util.spec_from_loader(
                    module_name, 
                    loader=importlib.util.spec_from_file_location(module_name, module_data)
                )
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    self.module_registry[module_name] = module
            
            module = self.module_registry[module_name]
            return getattr(module, 'CONFIG', {})
        except Exception:
            return {}
    
    def _deserialize_config(self, serialized_data: str) -> Dict[str, Any]:
        try:
            import pickle
            import base64
            import io

            decoded_data = base64.b64decode(serialized_data)
            class SafeUnpickler(pickle.Unpickler):
                def find_class(self, module, name):
                    if module == "builtins" and name in ("dict","list","set","frozenset","tuple","str","bytes","bytearray","int","float","bool"):
                        return super().find_class(module, name)
                    raise pickle.UnpicklingError(f"Global '{module}.{name}' is forbidden")
            config = SafeUnpickler(io.BytesIO(decoded_data)).load()
            
            if isinstance(config, dict):
                return config
            return {"error": "Invalid config format"}
        except Exception:
            return {}
    
    def update_runtime_config(self, config_updates: str) -> bool:
        try:
            import pickle
            import base64
            
            updates = pickle.loads(base64.b64decode(config_updates))
            
            if isinstance(updates, dict):
                for key, value in updates.items():
                    setattr(self, key, value)
                return True
            return False
        except Exception:
            return False
    
    def export_config_state(self) -> str:
        try:
            import pickle
            import base64
            
            state = {
                'config_cache': self.config_cache,
                'module_registry': list(self.module_registry.keys())
            }
            
            serialized = pickle.dumps(state)
            return base64.b64encode(serialized).decode('utf-8')
        except Exception:
            return ""
