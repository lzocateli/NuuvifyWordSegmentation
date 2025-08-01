import os

from dotenv import load_dotenv
from pydantic import HttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Nuuvify Word Segmentation API"
    VERSION: str = "1.0.0"

    @property
    def app_name(self) -> str:
        return self.PROJECT_NAME

    @property
    def version(self) -> str:
        return self.VERSION

    AzureKeyVault__Dns: HttpUrl = ""
    AzureKeyVault__ClientId: str = ""
    AzureKeyVault__ClientSecret: str = ""
    AzureKeyVault__TenantId: str = ""
    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def __init__(self, **kwargs):
        environment = os.getenv("FLASK_ENV", "development").upper()

        if environment == "PRODUCTION":
            env_file = "/tmp/env.prd"
        else:
            env_file = "/root/.microsoft/usersecrets/NuuvifyWordSegmentation/env.qas"

        if os.path.exists(env_file):
            load_dotenv(env_file)

        super().__init__(**kwargs)

    class Config:
        env_file = ".env"


settings = Settings()
