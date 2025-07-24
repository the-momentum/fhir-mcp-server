import os
from enum import Enum
from typing import Any, Callable, Generator, Protocol
from dotenv import load_dotenv

from cryptography.fernet import Fernet
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler

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
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        string_schema = core_schema.str_schema()
        return core_schema.no_info_after_validator_function(cls, string_schema)

    def __init__(self, value: str):
        super().__init__()
        self._secret_value = "".join(value.splitlines()).strip().encode("utf-8")
        self.decrypted = False

    def get_decrypted_value(self, decryptor: Decryptor) -> str:
        if not self.decrypted:
            try:
                value = decryptor.decrypt(self._secret_value)
                self._secret_value = value
                self.decrypted = True
            except Exception:
                # If decryption fails, assume it's already plain text
                pass
        return self._secret_value.decode("utf-8")


class FernetDecryptorField:
    def __init__(self, value: str):
        master_key = os.environ.get(value)
        if not master_key:
            self._decryptor = FakeFernet()
        else:
            self._decryptor = Fernet(master_key.encode())

    def decrypt(self, value: bytes) -> bytes:
        return self._decryptor.decrypt(value)
