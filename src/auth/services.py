import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import RefreshToken, User
from auth.security import hash_password, validate_password
from auth.schemas import UserAuthenticationSchema, UserRegistrationSchema
from config import settings


async def create_user(
    data: UserRegistrationSchema,
    session: AsyncSession,
) -> User:
    data.password = hash_password(data.password)
    insert_data = data.model_dump(by_alias=True)
    user = User(**insert_data)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(
    email: str,
    session: AsyncSession,
) -> User | None:
    stmt = select(User).where(User.email == email)
    result: Result = await session.execute(stmt)
    return result.scalars().first()


async def get_user_by_id(
    id: int,
    session: AsyncSession,
) -> User | None:
    user = await session.get(User, id)
    return user


async def authenticate_user(
    data: UserAuthenticationSchema,
    session: AsyncSession,
) -> User:
    user = await get_user_by_email(data.email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )
    if not validate_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials."
        )
    if user.is_blocked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The account is banned."
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="The account is deleted."
        )
    return user


async def create_refresh_token(
    user_id: int,
    session: AsyncSession,
    exp_delta: timedelta = timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS),
):
    refresh_token = RefreshToken(
        user_id=user_id,
        value=str(uuid.uuid4()),
        expires_at=datetime.utcnow() + exp_delta,
    )
    session.add(refresh_token)
    await session.commit()
    await session.refresh(refresh_token)
    return refresh_token


async def get_refresh_token(
    value: str,
    session: AsyncSession,
) -> RefreshToken | None:
    stmt = select(RefreshToken).where(RefreshToken.value == value)
    result = await session.execute(stmt)
    return result.scalars().first()


async def delete_refresh_token_by_value(
    value: str,
    session: AsyncSession,
) -> RefreshToken:
    stmt = (
        delete(RefreshToken).where(RefreshToken.value == value).returning(RefreshToken)
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.scalars().first()
