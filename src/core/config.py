import os
import urllib.parse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


env_file = None

if os.getenv("DOCKER_ENV") == "true":
    env_file = Path(__file__).resolve().parents[2] / "docker.env"
else:
    env_file = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    COIN_GECKO_API_KEY: str
    SECRET_KEY: str

    ALGORITHM: str = "HS256"
    JWT_REFRESH_EXPIRE_DAYS: int = 7
    JWT_ACCESS_EXPIRE_MIN: int = 30

    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str
    MONGO_INITDB_DATABASE: str
    MONGO_DB_PORT: int = 27017
    MONGO_DB_HOST: str
    MONGO_ADMIN_NAME: str = "admin"

    @property
    def MONGO_DB_URI(self):
        password = urllib.parse.quote_plus(self.MONGO_INITDB_ROOT_PASSWORD)
        return (
            f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:{password}@{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}/"
            f"{self.MONGO_INITDB_DATABASE}?authSource={self.MONGO_ADMIN_NAME}"
        )

    @property
    def BASE_MONGO_URI(self):
        return "mongodb://localhost:27017"

    model_config = SettingsConfigDict(env_file=env_file)

    @property
    def BASE_HEADERS(self) -> dict:
        return {
            "accept": "application/json",
            "x-cg-demo-api-key": settings.COIN_GECKO_API_KEY,
        }

    @property
    def BASE_COINS_API(self) -> str:
        return "https://api.coingecko.com/api/v3"


settings = Settings()  # type: ignore
