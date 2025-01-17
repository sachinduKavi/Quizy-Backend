from cryptography.fernet import  Fernet

key = b'OEYwS2JWTHmfB-PPUK8m6M70kUtSl9aRNjhFSejBNjM='
cipher_suite = Fernet(key)

def encrypt(message):
    return cipher_suite.encrypt(message.encode())

def decrypt(ciper):
    return cipher_suite.decrypt(ciper).decode()