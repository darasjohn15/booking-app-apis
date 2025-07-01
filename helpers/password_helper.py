import hashlib
import os
import base64

def hash_password(password: str) -> str:
    """
    Hash a password with a randomly generated salt using SHA-256.
    
    Returns:
        A base64-encoded string in the format: salt$hashed_password
    """
    salt = os.urandom(16)
    salt_b64 = base64.b64encode(salt).decode('utf-8')
    pwd_hash = hashlib.sha256(salt + password.encode()).digest()
    pwd_hash_b64 = base64.b64encode(pwd_hash).decode('utf-8')
    return f"{salt_b64}${pwd_hash_b64}"