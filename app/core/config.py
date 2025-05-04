from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

BASE_DIR = Path(__file__).resolve().parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    disable_docs: bool = False


class LogConfig(BaseModel):
    format: str = "%(name)s %(asctime)s %(levelname)s %(message)s"
    base_dir: str = "logs"
    backup_count: int = 5
    file_size: int = 5 * 1024 * 1024


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }


class MiniOConfig(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    bucket_name: str
    secure: bool

class KafkaConfig(BaseModel):
    endpoint:str


class ElasticConfig(BaseModel):
    endpoint: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=(".env.template", ".env", ".env.docker")
    )

    run: RunConfig
    elastic:ElasticConfig
    logs: LogConfig = LogConfig()
    miniO: MiniOConfig
    kafka: KafkaConfig


settings = Settings()
