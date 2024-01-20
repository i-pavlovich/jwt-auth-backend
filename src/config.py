from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    
    ALGORITHM: str = "RS256"
    JWT_PRIVATE_KEY_PATH: Path =  BASE_DIR / "certificates" / "jwt-private.pem"
    JWT_PUBLIC_KEY_PATH: Path = BASE_DIR / "certificates" / "jwt-public.pem"
    JWT_TOKEN_EXP_MINUTES: int = 15
    
    model_config = SettingsConfigDict(
        env_file=".env",
    )


settings = Settings()
