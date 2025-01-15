from cryptography.fernet import  Fernet

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt(message):
    return cipher_suite.encrypt(message.encode())

def decrypt(ciper):
    return cipher_suite.decrypt(ciper).decode()