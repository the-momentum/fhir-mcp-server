import os
from enum import Enum
from functools import wraps
from typing import Any, Callable, Generator, Protocol

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

CallableGenerator = Generator[Callable[..., Any], None, None]

dotenv_path = "config/.env"

load_dotenv(dotenv_path)


class EnvironmentType(str, Enum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


class Decryptor(Protocol):
    def decrypt(self, value: bytes) -> bytes: ...


class FakeFernet:
    def decrypt(self, value: bytes) -> bytes:
        return value


class EncryptedField(str):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: GetCoreSchemaHandler,
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


def set_env_from_settings(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to set environment variables from settings.
    This decorator is useful for encrypted fields and providers that
    require API keys to be available as environment variables.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        return func(*args, **kwargs)

    return wrapper
