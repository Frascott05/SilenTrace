from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        case_sensitive=True,
        extra="ignore"
    )

    APP_NAME: str = "SilentraceGUI"

    VOLATILITY_PATH: str
    DUMPS_PATH: str

    # 👇 STRINGA, NON LISTA
    ALLOWED_ORIGINS: str = "*"

    @property
    def allowed_origins_list(self):
        if self.ALLOWED_ORIGINS.strip() == "*":
            return ["*"]
        return [i.strip() for i in self.ALLOWED_ORIGINS.split(",")]


settings = Settings()