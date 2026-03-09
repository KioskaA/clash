from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    base_url: str = "http://localhost:8000/api/v1"
    use_mock: bool = True
    request_timeout: int = 30
    log_level: str = "INFO"
    token_service_name: str = "MyClashApp"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()