from functools import lru_cache
from pathlib import Path
from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.config_utils import EncryptedField, EnvironmentType, FernetDecryptorField


class Settings(BaseSettings):
    FERNET_DECRYPTOR: FernetDecryptorField = FernetDecryptorField("MASTER_KEY")

    PROJECT_NAME: str = "mcp-server"
    API_V1_STR: str = "/api/v1"
    LATEST_API_STR: str = API_V1_STR
    VERSION: str = "0.0.1"

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.TEST

    LOGGING_CONF_FILE: str = "logging.conf"

    # FHIR SERVER
    FHIR_SERVER_HOST: str = "https://api.medplum.com"
    FHIR_BASE_URL: str = "/fhir/R4"
    FHIR_SERVER_CLIENT_ID: str = ""
    FHIR_SERVER_CLIENT_SECRET: EncryptedField
    FHIR_SERVER_TIMEOUT: int = 20

    # LOINC
    LOINC_ENDPOINT: str = "https://loinc.regenstrief.org/searchapi/loincs"
    LOINC_USERNAME: str = ""
    LOINC_PASSWORD: EncryptedField
    LOINC_TIMEOUT: int = 60
    LOINC_MAX_CODES: int = 5
    LOINC_MAX_FETCH: int = 50

    PINECONE_API_KEY: EncryptedField
    PINECONE_NAMESPACE: str = "fhir-papers"
    PINECONE_INDEX_NAME: str = "fhir-mcp-server"
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"
    # RAG
    EMBEDDING_MODEL: str = "NeuML/pubmedbert-base-embeddings"
    VECTOR_DIMENSION: int = 768
    EMBED_METRIC: str = "cosine"
    EMBED_BATCH_SIZE: int = 96
    TOP_K_RETRIEVAL_RESULTS: int = 10

    @field_validator(
        "LOINC_PASSWORD", "FHIR_SERVER_CLIENT_SECRET", "PINECONE_API_KEY", mode="after"
    )
    def _decrypt_encrypted_fields(cls, v, validation_info: ValidationInfo):
        if isinstance(v, EncryptedField):
            decryptor = validation_info.data.get("FERNET_DECRYPTOR")
            if decryptor:
                return v.get_decrypted_value(decryptor)
        return v

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(Path(__file__).parent.parent / "config" / ".env"),
        extra="allow",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
