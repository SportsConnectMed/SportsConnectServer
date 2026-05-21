from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SportsConnectServer"
    debug: bool = False

    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )


settings = Settings()
