from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Astro Service API"
    DEBUG: bool = True

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

    # Default coords
    DEFAULT_COORDS: tuple = (55.7558, 37.6176)

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings,):
            return (init_settings, env_settings, file_secret_settings,)
        
        
settings = Settings()