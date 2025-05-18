from pydantic import BaseModel
from pydantic_settings import BaseSettings

class RunConfig(BaseModel):
    app: str = "main:main_app"
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False

class Settings(BaseSettings):
    run: RunConfig = RunConfig()

settings = Settings()