from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
        load values from .env
    """

    LITELLM_BASE_URL: str
    LITELLM_API_KEY: str
    MODEL_NAME: str

    model_config = SettingsConfigDict(
        env_file =".env",
        env_file_encoding ="utf-8"
    )


settings = Settings()