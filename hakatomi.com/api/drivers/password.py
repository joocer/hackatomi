import hashlib
from orso.tools import random_string

def generate_password_hash(password: str, salt: str, iterations: int = 100) -> str:
    """
    Generate a SHA-256 hash of the given password and salt, using multiple iterations to increase complexity.

    Parameters:
        password: str
            The password to hash.
        salt: str
            The salt to use in hashing.
        iterations: int, optional
            The number of hashing iterations to perform for added complexity (default is 100).

    Returns:
        str: A hexadecimal string representing the final SHA-256 hash.
    """
    # Initial hash with salt and password
    combined = salt + password
    hash_obj = hashlib.sha256(combined.encode())

    # Perform multiple iterations of SHA-256 hashing to increase complexity
    for _ in range(iterations - 1):
        # Include the salt in each iteration
        combined = salt + hash_obj.hexdigest()
        hash_obj = hashlib.sha256(combined.encode())

    # Final hash as a hexadecimal string
    final_hash = hash_obj.hexdigest()

    return final_hash

def generate_password():
    return random_string()