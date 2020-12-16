from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "phishpond"
    class Config:
        env_file = ".env"

settings = Settings()