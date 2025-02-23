from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    APP_NAME: str = "Astro Service API"
    DEBUG: bool = True
    
    LOG_PATH: str

    #Ephemeris
    EPHEMERIS_PATH: str = 'app/ephemeris'

    # Postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = 'gpt-4o'

    # Default coords
    DEFAULT_COORDS: tuple = (55.7558, 37.6176)
    DEFAULT_CITY: str = 'Москва'

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            init_settings,     # Значения, переданные при создании экземпляра
            env_settings,      # Переменные окружения
            dotenv_settings,   # Файл .env
            file_secret_settings,  # Секреты
        )
    
settings = Settings()