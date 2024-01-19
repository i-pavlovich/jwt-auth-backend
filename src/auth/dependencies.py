from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import services
from auth.schemas import UserRegistrationSchema
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
