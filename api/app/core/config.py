from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    fernet_key: str
    terraform_root: str = "/terraform"
    max_resources_per_provider: int = 1
    auto_destroy_hours: int = 24

    class Config:
        env_file = ".env"


settings = Settings()
