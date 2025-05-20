from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from .schemas import UserRegisterScheme, UserRead, UserLoginScheme
from . import crud

router = APIRouter()


@router.post("/login")
async def login(
    user: UserLoginScheme,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.authorization_user(
        user_data=user,
        session=session,
    )


@router.post(
    "/register",
    response_model=UserRead,
)
async def register(
    user: UserRegisterScheme,
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
):
    return await crud.user_registration(user_data=user, session=session)


@router.get("/profile")
async def profile():
    return {"message": "Login"}


@router.get("/logout")
async def logout():
    return {"message": "Logout"}
