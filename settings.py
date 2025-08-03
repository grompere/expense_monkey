from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from functools import cached_property

# Shared configuration to reduce repetition
_BASE_CONFIG = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore"
)

class GoogleSettings(BaseSettings):
    """Google API configuration"""
    api_key: Optional[str] = Field(None, description="Google Gemini API key")
    
    model_config = SettingsConfigDict(
        **_BASE_CONFIG,
        env_prefix="GOOGLE_"
    )

class AppSettings(BaseSettings):
    """Main application settings that combines all configurations"""
    
    environment: str = Field("development", description="Application environment")
    debug: bool = Field(False, description="Enable debug mode")
    
    model_config = _BASE_CONFIG
    
    @cached_property
    def google(self) -> GoogleSettings:
        """Lazy-loaded Google settings"""
        return GoogleSettings()

_settings_instance: Optional[AppSettings] = None

def get_settings() -> AppSettings:
    """Get the global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = AppSettings()
    return _settings_instance 