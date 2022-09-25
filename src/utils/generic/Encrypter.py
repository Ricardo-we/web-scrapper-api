
from cryptography.fernet import Fernet

key = Fernet.generate_key()
fernet = Fernet(key)


class Encrypter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def encrypt(value: str):
        return fernet.encrypt(value.encode("utf-8"))

    @staticmethod
    def decrypt(value: str):
        return fernet.decrypt(value)
