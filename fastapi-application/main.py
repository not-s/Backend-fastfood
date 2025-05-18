import uvicorn
from fastapi import FastAPI

from core.config import settings

main_app = FastAPI()


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
