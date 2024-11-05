# src/config/settings.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Pancake POS configs
    PANCAKE_API_KEY: str
    PANCAKE_BASE_URL: str = "https://pos.pages.fm/api/v1"
    PANCAKE_SHOP_ID: str
    PANCAKE_WEBHOOK_SECRET: str

    # Dify configs
    DIFY_API_KEY: str
    DIFY_BASE_URL: str
    DIFY_APP_ID: str

    class Config:
        env_file = ".env"

settings = Settings()