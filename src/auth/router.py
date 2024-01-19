from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.dependencies import valid_user_registration
from auth.models import User
from auth.schemas import UserRegistrationSchema, UserSchema
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
