from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import base64
import os

def generate_salt() -> bytes:
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(plaintext: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(plaintext.encode())

def decrypt(ciphertext: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(ciphertext).decode()