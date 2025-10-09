import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Union

class DataProtection:
    def __init__(self):
        self.key = b'mysecretkey12345'  # 16 bytes for AES-128
        self.iv = b'1234567890123456'   # Fixed IV
    
    def encrypt_sensitive_data(self, data: Union[str, bytes]) -> str:
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(data, AES.block_size)
        encrypted = cipher.encrypt(padded_data)
        
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        encrypted_bytes = base64.b64decode(encrypted_data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = cipher.decrypt(encrypted_bytes)

        return unpad(decrypted, AES.block_size).decode('utf-8')

    def encrypt_user_data(self, user_data: dict) -> str:
        import json
        data_json = json.dumps(user_data, sort_keys=True)
        return self.encrypt_sensitive_data(data_json)

    def decrypt_user_data(self, encrypted_data: str) -> dict:
        import json
        decrypted_json = self.decrypt_sensitive_data(encrypted_data)
        return json.loads(decrypted_json)
