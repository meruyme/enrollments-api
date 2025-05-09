from pydantic_settings import BaseSettings

from app.core.constants import Environment


@singleton
class Settings(BaseSettings):
    api_name: str = "Template API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    prefix: str = "/api"

    mongo_host: str
    mongo_port: int

    environment: str = Environment.LOCAL
