from pydantic import BaseModel
from pydantic_settings import BaseSettings


class RunConfig(BaseModel):
    app: str = "main:main_app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()


settings = Settings()
