from datetime import datetime

from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.models import RefreshToken, User
from auth.schemas import UserRegistrationSchema
from config import settings
from database import get_session


async def valid_user_registration(
    data: UserRegistrationSchema,
    session: AsyncSession = Depends(get_session),
) -> UserRegistrationSchema:
    if await services.get_user_by_email(data.email, session) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already taken.",
        )
    return data


def valid_refresh_token_exp_time(
    refresh_token: RefreshToken,
) -> bool:
    return datetime.utcnow() <= refresh_token.expires_at


async def valid_refresh_token(
    refresh_token_value: str = Cookie(alias=settings.REFRESH_TOKEN_COOKIE_KEY),
    session: AsyncSession = Depends(get_session),
) -> RefreshToken:
    refresh_token = await services.get_refresh_token(refresh_token_value, session)
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is not valid.",
        )
    if not valid_refresh_token_exp_time(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is not valid.",
        )
    return refresh_token


async def valid_refresh_token_user(
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await services.get_user_by_id(refresh_token.user_id, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is not valid.",
        )
    return user
