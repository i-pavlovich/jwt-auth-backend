from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from auth.security import hash_password
from auth.schemas import UserRegistrationSchema


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
