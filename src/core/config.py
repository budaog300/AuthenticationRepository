from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsDB(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    ACCESS_SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_url_db(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def get_auth_data(self) -> dict:
        return {"access_secret_key": self.ACCESS_SECRET_KEY, "refresh_secret_key": self.ACCESS_SECRET_KEY, "algorithm": self.ALGORITHM}
     

settings = SettingsDB()