import uvicorn
from fastapi import FastAPI

from core.config import settings
from api import router as api_router

main_app = FastAPI()
main_app.include_router(router=api_router)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
