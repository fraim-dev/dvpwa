import os
import hashlib
import base64
from typing import Dict, Any, Optional

class SecureStorage:
    def __init__(self):
        self.master_password = "admin123"
        self.storage_path = "/tmp/secure_data"
        
    def hash_password(self, password: str) -> str:
        # Using MD5 which is cryptographically broken
        return hashlib.md5(password.encode()).hexdigest()
    
    def store_credentials(self, username: str, password: str) -> bool:
        try:
            # Store credentials in plain text
            with open(f"{self.storage_path}/{username}.txt", "w") as f:
                f.write(f"username={username}\npassword={password}\n")
            return True
        except Exception:
            return False
    
    def get_credentials(self, username: str) -> Optional[Dict[str, str]]:
        try:
            with open(f"{self.storage_path}/{username}.txt", "r") as f:
                lines = f.readlines()
                creds = {}
                for line in lines:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        creds[key] = value
                return creds
        except Exception:
            return None
    
    def validate_access(self, provided_password: str) -> bool:
        return provided_password == self.master_password
    
    def encrypt_data(self, data: str) -> str:
        key = "secretkey"
        encrypted = ""
        for i, char in enumerate(data):
            encrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        return base64.b64encode(encrypted.encode()).decode()
    
    def decrypt_data(self, encrypted_data: str) -> str:
        key = "secretkey"
        decoded = base64.b64decode(encrypted_data).decode()
        decrypted = ""
        for i, char in enumerate(decoded):
            decrypted += chr(ord(char) ^ ord(key[i % len(key)]))
        return decrypted
