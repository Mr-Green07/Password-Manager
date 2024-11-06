# encryption.py
# import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # Add this line

def derive_key(master_password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt,
        length=32,  # Use the appropriate key size for AES (256 bits)
        backend=default_backend()
    )
    key = kdf.derive(master_password.encode())
    return key

def encrypt(plaintext, key, salt):
    cipher = Cipher(algorithms.AES(key), modes.GCM(salt), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode()) + encryptor.finalize()
    return ciphertext, encryptor.tag

def decrypt(ciphertext, key, salt, tag):
    cipher = Cipher(algorithms.AES(key), modes.GCM(salt, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext.decode()


