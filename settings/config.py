from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    LOG_LEVEL: str = Field(default="INFO")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    # Database
    SQLALCHEMY_DATABASE_URI: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/xhorizon"
    )
    DB_ECHO: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=5)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_TIMEOUT: int = Field(default=30)

    # App timezone for scheduled jobs (calculations run in Moscow time)
    APP_TIMEZONE: str = Field(default="Europe/Moscow")

    # Auth / JWT
    JWT_SECRET_KEY: str = Field(default="dev-secret-change-me")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    class Config:
        env_file = ".env"
        case_sensitive = True


config = Config()