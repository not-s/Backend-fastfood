from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from auth import utils as auth_utils
import logging

from core.models import User
from .schemas import UserRegisterScheme


async def validation_user_registration(
    user_data: UserRegisterScheme,
    session: AsyncSession,
) -> None:
    # проверка на существующего пользователя
    stmt = select(User).where(
        or_(
            User.email == user_data.email,
            User.phone == user_data.phone if user_data.phone else False,
        )
    )

    existing_user = await session.execute(stmt)
    existing_user = existing_user.scalar()
    if existing_user is not None:
        detail = "Email уже зарегистрирован"
        if (
            existing_user.email != user_data.email
            and user_data.phone
            and existing_user.phone == user_data.phone
        ):
            detail = "Номер телефона уже зарегистрирован"

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


async def user_registration(
    user_data: UserRegisterScheme,
    session: AsyncSession,
) -> User:
    await validation_user_registration(
        user_data=user_data,
        session=session,
    )
    try:
        # создание пользователя
        user = User(
            email=user_data.email,
            password=auth_utils.hash_password(user_data.password),
            phone=user_data.phone,
            username=user_data.username,
            family_name=user_data.family_name,
            birthday=user_data.birthday,
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        logging.info(f"Пользователь с email {user.email} успешно зарегистрирован")
        return user
    except Exception as e:
        await session.rollback()
        logging.error(f"Ошибка при регистрации пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при регистрации пользователя",
        )
