from pydantic_settings import BaseSettings

from app.core.constants import Environment


class Settings(BaseSettings):
    api_name: str = "Enrollments API"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int
    prefix: str = "/api"
    credentials_path: str = "credentials.json"

    mongo_host: str
    mongo_port: int
    database_name: str

    age_group_api_base_url: str
    age_group_api_username: str
    age_group_api_password: str

    environment: str = Environment.LOCAL
