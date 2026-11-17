"""The original source phrase, converted to Fernet's required key format."""
import base64
import hashlib

from cryptography.fernet import Fernet

KEY_PHRASE = 'Hello! You found the secret message! Contact secretmessage@usc.edu to claim your reward!'


def make_cipher():
    # SHA-256 produces 32 BYTES (256 bits), then URL-safe base64 encodes them.
    # This is intentionally a source-embedded key, as requested for this app.
    key = base64.urlsafe_b64encode(hashlib.sha256(KEY_PHRASE.encode('utf-8')).digest())
    return Fernet(key)
