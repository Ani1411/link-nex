import string
import random
import hashlib
import secrets
from datetime import datetime, timezone

# Base62 characters (a-z, A-Z, 0-9) - excludes + and / for URL safety
BASE62_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits

def generate_short_code(length: int = 6) -> str:
    """Generate a random short code for URL shortening (fallback method)"""
    return ''.join(random.choice(BASE62_CHARS) for _ in range(length))

def generate_hash_based_code(original_url: str, length: int = 6) -> str:
    """Generate deterministic short code using hash function with salt"""
    # Add salt (timestamp + secret) for entropy and prevent preimage attacks
    salt = f"{secrets.token_hex(8)}_{datetime.now(timezone.utc).isoformat()}"
    
    # Create hash input with URL and salt
    hash_input = f"{original_url}_{salt}".encode('utf-8')
    
    # Generate SHA-256 hash
    hash_digest = hashlib.sha256(hash_input).hexdigest()
    
    # Convert hex to base62 and take first N characters
    return hex_to_base62(hash_digest)[:length]

def hex_to_base62(hex_string: str) -> str:
    """Convert hexadecimal string to base62 encoding"""
    # Convert hex to integer
    num = int(hex_string, 16)
    
    if num == 0:
        return BASE62_CHARS[0]
    
    result = []
    while num > 0:
        result.append(BASE62_CHARS[num % 62])
        num //= 62
    
    return ''.join(reversed(result))

def generate_entropy_code(original_url: str, length: int = 6) -> str:
    """Generate short code with high entropy using URL + random nonce"""
    # Use cryptographically secure random nonce
    nonce = secrets.token_bytes(16)
    
    # Combine URL with nonce for hash input
    hash_input = original_url.encode('utf-8') + nonce
    
    # Generate SHA-256 hash
    hash_digest = hashlib.sha256(hash_input).hexdigest()
    
    # Convert to base62 and truncate
    return hex_to_base62(hash_digest)[:length]