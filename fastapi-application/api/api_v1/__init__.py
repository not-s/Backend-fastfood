from fastapi import APIRouter

from core.config import settings

from .auth_jwt.views import router as auth_jwt_router
from .menu.menu_views import router as menu_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
    tags=["api V1"],
)
router.include_router(
    router=auth_jwt_router,
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)

router.include_router(
    router=menu_router,
    prefix=settings.api.v1.menu,
    tags=["Menu"],
)
