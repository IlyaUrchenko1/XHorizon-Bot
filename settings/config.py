from pydantic import Field
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    LOG_LEVEL: str = Field(default="INFO")
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)

    class Config:
        env_file = ".env"
        case_sensitive = True

config = Config()