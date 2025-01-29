from cryptography.fernet import Fernet

# Encryption key (ensure this is kept secret and secure)
key = b'OEYwS2JWTHmfB-PPUK8m6M70kUtSl9aRNjhFSejBNjM='
cipher_suite = Fernet(key)

def encrypt(message):
    """
    Encrypt a message (string) and return the encrypted bytes as a string.
    """
    return cipher_suite.encrypt(message.encode()).decode()  # Convert bytes to string for storage

def decrypt(ciper):
    """
    Decrypt the cipher text and return the original message as an integer.
    """
    if not ciper:
        raise ValueError("Cipher text is None or empty.")

    # Ensure the cipher text is properly formatted for decryption
    if isinstance(ciper, str) and ciper.startswith("b'") and ciper.endswith("'"):
        ciper = ciper[2:-1]  # Remove the wrapping b' and '

    # Attempt decryption
    try:
        decrypted_message = cipher_suite.decrypt(ciper.encode()).decode()  # Decrypt and decode
        return int(decrypted_message)  # Convert the decrypted message to an integer
    except Exception as e:
        raise ValueError(f"Failed to decrypt cipher text: {e}")
