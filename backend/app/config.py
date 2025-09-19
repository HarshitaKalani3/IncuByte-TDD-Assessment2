from pydantic_settings import BaseSettings
from pydantic import ConfigDict
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://harshi:123h@localhost:5432/sweetshop"
    SECRET_KEY: str = "harshitaa"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    model_config = ConfigDict(env_file=".env")
def get_settings():
    return Settings()