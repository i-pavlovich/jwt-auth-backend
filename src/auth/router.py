from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_registration,
)
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


@router.post("/refresh_tokens")
async def refresh_tokens(
    response: Response,
    background_tasks: BackgroundTasks,
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    user: User = Depends(valid_refresh_token_user),
    session: AsyncSession = Depends(get_session),
) -> TokenResponseSchema:
    new_refresh_token: RefreshToken = await services.create_refresh_token(
        refresh_token.user_id, session
    )
    cookie_settings = get_refresh_token_cookie_settings(new_refresh_token)
    response.set_cookie(**cookie_settings)
    background_tasks.add_task(
        services.delete_refresh_token_by_value,
        value=refresh_token.value,
        session=session,
    )
    return TokenResponseSchema(
        access_token=encode_jwt(user), refresh_token=new_refresh_token.value
    )

@router.delete("/logout")
def user_logout(
    response: Response,
    background_tasks: BackgroundTasks,
    refresh_token: RefreshToken = Depends(valid_refresh_token),
    session: AsyncSession = Depends(get_session),
) -> None:
    cookie_settings = get_refresh_token_cookie_settings(refresh_token)
    response.delete_cookie(cookie_settings.get("key"))
    background_tasks.add_task(
        services.delete_refresh_token_by_value,
        value=refresh_token.value,
        session=session,
    )