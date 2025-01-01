import urllib.parse
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    COIN_GECKO_API_KEY: str

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

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env"
    )


settings = Settings()  # type: ignore
