"""Configuration settings for the application."""
import os
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    google_api_key: str = os.getenv("GOOGLE_API_KEY", "")
    twitter_api_key: str = os.getenv("TWITTER_API_KEY", "")
    twitter_api_secret: str = os.getenv("TWITTER_API_SECRET", "")
    twitter_access_token: str = os.getenv("TWITTER_ACCESS_TOKEN", "")
    twitter_access_token_secret: str = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    
    # Optional configuration
    max_tweets_per_thread: int = int(os.getenv("MAX_TWEETS_PER_THREAD", "10"))
    research_depth: str = os.getenv("RESEARCH_DEPTH", "comprehensive")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    model_config = {
        "env_file": ".env",
        "extra": "allow"
    }

settings = Settings() 