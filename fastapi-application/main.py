from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from api import router as api_router
from core.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)
main_app.include_router(router=api_router)


if __name__ == "__main__":
    uvicorn.run(
        app=settings.run.app,
        host=settings.run.host,
        port=settings.run.port,
        reload=settings.run.reload,
    )
