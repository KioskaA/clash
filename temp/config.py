from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    COC_API_LOGIN: str
    COC_API_PASSWORD: str
    CLANTAG: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def coc_api(self) -> dict:
        return {
            "login": self.COC_API_LOGIN,
            "password": self.COC_API_PASSWORD,
            "clantag": self.CLANTAG,
        }


settings = Settings()