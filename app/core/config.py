import os
from typing import List
from pydantic import AnyHttpUrl, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.config_utils import EncryptedField, EnvironmentType


class Settings(BaseSettings):
    # FERNET_DECRYPTOR: FernetDecryptorField = Field("MASTER_KEY")

    PROJECT_NAME: str = "mcp-server"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.0.1"

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.TEST

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    BACKEND_CORS_ALLOW_ALL: bool = False

    LOGGING_CONF_FILE: str = "logging.conf"

    DATABASE_URI: str = ""  # TODO add db if required

    @field_validator("*", mode="after")
    def _decryptor(cls, v, validation_info: ValidationInfo, *args, **kwargs):
        if isinstance(v, EncryptedField):
            return v.get_decrypted_value(validation_info.data["FERNET_DECRYPTOR"])
        return v

    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=os.environ.get("ENV", ".env"),
        extra="allow",
    )


settings = Settings()  # type: ignore
