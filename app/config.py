from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.utils.config_utils import (
    EncryptedField,
    EnvironmentType,
    FernetDecryptorField,
    set_env_from_settings,
)

type OAuth2AuthMethod = Literal["client_credentials", "authorization_code"]
type TransportMode = Literal["stdio", "http", "https"]


class Settings(BaseSettings):
    FERNET_DECRYPTOR: FernetDecryptorField | None = FernetDecryptorField("MASTER_KEY")

    PROJECT_NAME: str = "mcp-server"
    API_V1_STR: str = "/api/v1"
    LATEST_API_STR: str = API_V1_STR
    VERSION: str = "0.0.1"

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentType = EnvironmentType.TEST

    LOGGING_CONF_FILE: str = "logging.conf"

    # MCP SERVER
    TRANSPORT_MODE: TransportMode = "stdio"
    MCP_SERVER_HOST: str = "localhost"
    MCP_SERVER_PORT: int = 8000
    MCP_SERVER_SSL_KEYFILE: str = "./localhost-key.pem"
    MCP_SERVER_SSL_CERTFILE: str = "./localhost.pem"

    # OAuth2 Configuration
    OAUTH2_AUTH_METHOD: OAuth2AuthMethod = "client_credentials"
    OAUTH2_REDIRECT_URI: str = ""
    OAUTH2_SCOPE: str = "openid"

    # FHIR SERVER
    FHIR_SERVER_HOST: str = "https://api.medplum.com"
    FHIR_BASE_URL: str = "/fhir/R4"
    FHIR_SERVER_CLIENT_ID: str = ""
    FHIR_SERVER_CLIENT_SECRET: EncryptedField = EncryptedField("")
    FHIR_SERVER_TIMEOUT: int = 20

    # LOINC
    LOINC_ENDPOINT: str = "https://loinc.regenstrief.org/searchapi/loincs"
    LOINC_USERNAME: str = ""
    LOINC_PASSWORD: EncryptedField = EncryptedField("")
    LOINC_TIMEOUT: int = 60
    LOINC_MAX_CODES: int = 5
    LOINC_MAX_FETCH: int = 50

    PINECONE_API_KEY: EncryptedField = EncryptedField("")
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
        "LOINC_PASSWORD",
        "FHIR_SERVER_CLIENT_SECRET",
        "PINECONE_API_KEY",
        mode="after",
    )
    @classmethod
    def _decrypt_encrypted_fields(
        cls,
        v: EncryptedField,
        validation_info: ValidationInfo,
    ) -> str | EncryptedField:
        fernet_decryptor = validation_info.data.get("FERNET_DECRYPTOR")
        if fernet_decryptor:
            decrypted_value = v.get_decrypted_value(fernet_decryptor)
            return str(decrypted_value)
        return v

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(Path(__file__).parent.parent / "config" / ".env"),
        extra="allow",
    )


@lru_cache
@set_env_from_settings
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


settings = get_settings()
