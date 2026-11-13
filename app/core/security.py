
from pwdlib import PasswordHash


# Initialize Argon2 password hashing
password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    """
    Hash a plain-text password and return the hashed password.

    :param password: plain-text password
    :return: hashed password
    """
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against a hashed password.
    :param plain_password: The plain-text password to verify
    :param hashed_password: The hashed password to verify
    :return: a boolean value indicating whether the password matches the hashed password or not.
    """

    return password_hash.verify(
        plain_password,
        hashed_password
    )