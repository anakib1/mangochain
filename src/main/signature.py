from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa


# Generate a private/public key pair

def sign_message(message, private_key):
    message_bytes = bytes.fromhex(message)
    signature = private_key.sign(
        message_bytes,
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return signature


def verify_signature(message, signature, public_key):
    message_bytes = bytes.fromhex(message)
    try:
        public_key.verify(
            signature,
            message_bytes,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print("Signature verification failed:", e)
        return False
