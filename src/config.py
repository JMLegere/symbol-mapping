from pydantic import BaseSettings


class Settings(BaseSettings):
    openfigi_api_key: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()
