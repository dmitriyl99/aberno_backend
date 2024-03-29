from pydantic_settings import BaseSettings

import dotenv

dotenv.load_dotenv(".env")


class _Settings(BaseSettings):
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    database_port: int

    secret_key: str
    access_token_expires_minutes: int = 86400
    jwt_algorithm: str


settings = _Settings()


TORTOISE_ORM = {
    "connections": {
        "default":
            f"postgres://"
            f"{settings.database_user}:"
            f"{settings.database_password}@"
            f"{settings.database_host}:"
            f"{settings.database_port}/{settings.database_name}"},
    "apps": {
        "models": {
            "models": [
                'app.core.models.auth.user',
                'app.core.models.auth.permission',
                'app.core.models.auth.role',

                'app.core.models.organization.department',
                'app.core.models.organization.employee',
                'app.core.models.organization.organization',
                'aerich.models'
            ],
            "default_connection": "default"
        }
    }
}
