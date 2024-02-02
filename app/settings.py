from pydantic_settings import BaseSettings

import dotenv

dotenv.load_dotenv(".env")


class _Settings(BaseSettings):
    database_host: str
    database_user: str
    database_password: str
    database_name: str

    secret_key: str
    access_token_expires_minutes: int = 86400
    jwt_algorithm: str


settings = _Settings()
