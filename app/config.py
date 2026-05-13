from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://app:app@localhost:5432/shopping_db"
    api_prefix: str = "/shopping"
    service_name: str = "shopping-list"

    pantry_internal_url: str = "http://localhost:8000/pantry"
    pantry_request_timeout_seconds: float = 5.0


settings = Settings()
