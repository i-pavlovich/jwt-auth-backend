from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class JWTPayloadSchema(BaseModel):
    sub: str
    exp: datetime
    is_admin: bool


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class UserAuthenticationSchema(BaseModel):
    email: EmailStr
    password: str


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
