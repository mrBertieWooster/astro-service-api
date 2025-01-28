from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Astro Service API"
    DEBUG: bool = True

    #Ephemeris
    EPHEMERIS_PATH: str

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"

    @property
    def EPHEMERIS_PATH(self) -> str:
        return self.EPHEMERIS_PATH

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = ".env"

settings = Settings()