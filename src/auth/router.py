from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.dependencies import valid_user_registration
from auth.models import RefreshToken, User
from auth.schemas import (
    TokenResponseSchema,
    UserAuthenticationSchema,
    UserRegistrationSchema,
    UserSchema,
)
from auth.utils import encode_jwt, get_refresh_token_cookie_settings
from database import get_session


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/registration", status_code=status.HTTP_201_CREATED)
async def user_registration(
    data: UserRegistrationSchema = Depends(valid_user_registration),
    session: AsyncSession = Depends(get_session),
) -> UserSchema:
    user: User = await services.create_user(data, session)
    return user


@router.post("/authentication")
async def user_authentication(
    data: UserAuthenticationSchema,
    response: Response,
    session: AsyncSession = Depends(get_session),
) -> TokenResponseSchema:
    user: User = await services.authenticate_user(data, session)
    refresh_token: RefreshToken = await services.create_refresh_token(user.id, session)
    cookie_settings = get_refresh_token_cookie_settings(refresh_token)
    response.set_cookie(**cookie_settings)
    return TokenResponseSchema(
        access_token=encode_jwt(user), refresh_token=refresh_token.value
    )
