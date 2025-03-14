from pydantic import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Decentralized Content Moderation Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Blockchain settings
    BLOCKCHAIN_PROVIDER_URL: str = os.getenv(
        "BLOCKCHAIN_PROVIDER_URL", "http://localhost:8545"
    )
    SMART_CONTRACT_ADDRESS: str = os.getenv("SMART_CONTRACT_ADDRESS", "")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./content_moderation.db")

    # AI Model settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/content_moderation")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.8"))

    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
