from cryptography.fernet import Fernet

key = b'OEYwS2JWTHmfB-PPUK8m6M70kUtSl9aRNjhFSejBNjM='
cipher_suite = Fernet(key)

def encrypt(message):
    # Encrypt the message (string) and return the encrypted bytes
    return cipher_suite.encrypt(message.encode())

def decrypt(ciper):
    # Strip the byte format
    if ciper.startswith("b'") and ciper.endswith("'"):
        ciper = ciper[2:-1]
        # Convert the cipher text (string) to bytes, decrypt it, decode to plaintext, and convert to int
    return int(cipher_suite.decrypt(ciper.encode()).decode())