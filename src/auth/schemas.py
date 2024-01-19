from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegistrationSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(serialization_alias="password_hash")

    name: Optional[str]
    surname: Optional[str]


class UserSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    username: str
    email: EmailStr

    name: Optional[str]
    surname: Optional[str]

    is_active: bool
    is_admin: bool
    is_blocked: bool
