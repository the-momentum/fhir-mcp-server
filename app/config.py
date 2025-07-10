from functools import lru_cache
from pathlib import Path
from pydantic import AnyHttpUrl, ValidationInfo, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.config_utils import EncryptedField, EnvironmentType


class Settings(BaseSettings):
    # FERNET_DECRYPTOR: FernetDecryptorField = Field("MASTER_KEY")

    PROJECT_NAME: str = "mcp-server"
    API_V1_STR: str = "/api/v1"
    LATEST_API_STR: str = API_V1_STR
    VERSION: str = "0.0.1"

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.TEST

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    BACKEND_CORS_ALLOW_ALL: bool = False

    LOGGING_CONF_FILE: str = "logging.conf"

    DATABASE_URI: str = ""  # TODO add db if required

    # MEDPLUM
    MEDPLUM_HOST: str = "https://api.medplum.com"
    FHIR_BASE_URL: str = "/fhir/R4"
    MEDPLUM_APP_URL: str = "https://app.medplum.com"
    MEDPLUM_CLIENT_ID: str = ""
    MEDPLUM_CLIENT_SECRET: SecretStr = SecretStr("")
    MEDPLUM_TIMEOUT: int = 20

    # LOINC
    LOINC_ENDPOINT: str = "https://loinc.regenstrief.org/searchapi/loincs"
    LOINC_USERNAME: str = ""
    LOINC_PASSWORD: SecretStr = SecretStr("")
    LOINC_TIMEOUT: int = 60
    LOINC_MAX_CODES: int = 5
    LOINC_MAX_FETCH: int = 50

    PINECONE_API_KEY: SecretStr = SecretStr("")
    PINECONE_NAMESPACE: str = "fhir-papers"
    PINECONE_INDEX_NAME: str = "fhir-mcp-server"
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"
    # RAG
    EMBEDDING_MODEL: str = "NeuML/pubmedbert-base-embeddings"
    VECTOR_DIMENSION: int = 768
    EMBED_METRIC: str = "cosine"
    EMBED_BATCH_SIZE: int = 96

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
        env_file=str(Path(__file__).parent.parent / "config" / ".env"),
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
