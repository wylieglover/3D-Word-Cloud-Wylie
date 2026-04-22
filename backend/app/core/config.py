from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8000
    database_url: str
    frontend_url: str

    jwt_access_secret: str = Field(min_length=32)
    jwt_refresh_secret: str = Field(min_length=32)

    jwt_refresh_expire_minutes: int = 60 * 24 * 7
    jwt_access_expire_minutes: int = 15

    class Config: 
        env_file = ".env"

settings = Settings()