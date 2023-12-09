from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./mydatabase.db"
    secret_key: str = "12b47320393cafd269a011a4c1cf29949b865e859512fbb0461db71e31b67399"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
