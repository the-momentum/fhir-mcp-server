import os
from enum import Enum
from typing import Any, Callable, Generator, Protocol
from dotenv import load_dotenv

from cryptography.fernet import Fernet
from pydantic import ValidationInfo

CallableGenerator = Generator[Callable[..., Any], None, None]

dotenv_path = "config/.env"

load_dotenv(dotenv_path)


class EnvironmentType(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Decryptor(Protocol):
    def decrypt(self, value: bytes) -> bytes: ...  # fmt: skip


class FakeFernet:
    def decrypt(self, value: bytes) -> bytes:
        return value


class EncryptedField(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type="str", writeOnly=True)

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: str, validation_info: ValidationInfo) -> "EncryptedField":
        if isinstance(value, cls):
            return value
        return cls(value)

    def __init__(self, value: str):
        self._secret_value = "".join(value.splitlines()).strip().encode("utf-8")
        self.decrypted = False

    def get_decrypted_value(self, decryptor: Decryptor) -> str:
        if not self.decrypted:
            value = decryptor.decrypt(self._secret_value)
            self._secret_value = value
            self.decrypted = True
        return self._secret_value.decode("utf-8")


class FernetDecryptorField(str):
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any]) -> None:
        field_schema.update(type="str", writeOnly=True)

    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: str, validation_info: ValidationInfo) -> Decryptor:
        master_key = os.environ.get(value)
        if not master_key:
            return FakeFernet()
        return Fernet(master_key.encode())
