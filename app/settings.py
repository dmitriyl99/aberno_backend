import os

from pydantic_settings import BaseSettings

import dotenv

dotenv.load_dotenv(".env")


class _Settings(BaseSettings):
    environment: str
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    database_port: int

    secret_key: str
    access_token_expires_minutes: int = 86400
    jwt_algorithm: str


settings = _Settings()
