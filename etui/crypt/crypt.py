import logging
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken

__all__ = ["encrypt", "decrypt"]

logger = logging.getLogger(__name__)
sf = ".crypt"


def generate_key() -> str:
    key = Fernet.generate_key()
    return key


def loaad_key() -> str:
    with open(sf, "r") as f:
        return f.read()


def store_key(key: str) -> None:
    """Stores the key in a file with name .crypt. Not secure and should be used for testing and local usage only."""
    with open(sf, "wb") as f:
        f.write(key)


def is_key_valid(key: str, value: str) -> bool:
    try:
        Fernet(key).decrypt(value.encode())
        return True
    except InvalidToken as it:
        logger.debug(it)
        return False


def get_key() -> str:
    if Path(sf).exists():
        return loaad_key()
    else:
        logger.info("Key does not exist, generating..")
        key = generate_key()
        store_key(key)
        logger.info("Key stored")
        return key


def encrypt(input: str) -> str:
    key = get_key()
    return Fernet(key).encrypt(input.encode()).decode()


def decrypt(input: str) -> str:
    key = get_key()
    if not is_key_valid(key, input):
        logging.error("Key not valid for decryption")
        exit()
    return Fernet(key).decrypt(input.encode()).decode()


if __name__ == "__main__":
    operation = input("Encrypt or Decrypt: ")
    if operation not in ["encrypt", "decrypt"]:
        logging.error("Invalid operation")
        exit()
    input = input("Input: ")

    if operation.lower() == "encrypt":
        out = encrypt(input)
    elif operation.lower() == "decrypt":
        out = decrypt(input)

    print(out)
