from fastapi import HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from auth import utils as auth_utils
import logging
import uuid

from core.models import User, Token
from .schemas import UserRegisterScheme, UserLoginScheme, LoginResponseScheme


async def authorization_user(
    user_data: UserLoginScheme,
    session: AsyncSession,
):
    # Проверка пользователя
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    stmt = select(User).where(User.email == user_data.email)
    if not (user := await session.scalar(stmt)):
        raise unauthed_exc
    elif not auth_utils.validate_password(
        password=user_data.password,
        hashed_password=user.password,
    ):
        raise unauthed_exc

    # Создание JWT
    jwt_payload = {
        "sub": user.id,
        "email": user.email,
        "jti": str(uuid.uuid4()),
    }
    token = auth_utils.encode_jwt(jwt_payload)

    # Проверка количество токенов
    token_query = await session.execute(select(Token).where(Token.user_id == user.id))
    active_tokens = token_query.scalars().all()

    if len(active_tokens) >= 10:
        for user_data_token in active_tokens[: len(active_tokens) - 9]:
            await session.delete(user_data_token)

    # сохранение jti токена
    try:
        token_info = Token(
            user_id=user.id,
            jti=jwt_payload["jti"],
        )
        session.add(token_info)
        await session.commit()
    except Exception as e:
        await session.rollback()
        logging.error(f"Ошибка при создании токена: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при авторизации",
        )

    return LoginResponseScheme(
        access_token=token, email=user.email, token_type="bearer"
    )


async def validation_user_registration(
    user_data: UserRegisterScheme,
    session: AsyncSession,
) -> None:
    # проверка на существующего пользователя
    conditions = [User.email == user_data.email]
    if user_data.phone:
        conditions.append(User.phone == user_data.phone)
    stmt = select(User).where(or_(*conditions))

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
    except IntegrityError as e:
        await session.rollback()
        logging.error(f"Ошибка целостности данных: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при сохранении данных пользователя",
        )

    except Exception as e:
        await session.rollback()
        logging.error(f"Ошибка при регистрации пользователя: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при регистрации пользователя",
        )
