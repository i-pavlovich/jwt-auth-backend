from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.dependencies import valid_user_registration
from auth.jwt import encode_jwt
from auth.models import User
from auth.schemas import (
    TokenResponseSchema,
    UserAuthenticationSchema,
    UserRegistrationSchema,
    UserSchema,
)
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
    session: AsyncSession = Depends(get_session),
) -> TokenResponseSchema:
    user: User = await services.authenticate_user(data, session)
    access_token = encode_jwt(user)
    return TokenResponseSchema(access_token=access_token)
