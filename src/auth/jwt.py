from datetime import datetime, timedelta

import jwt

from auth.models import User
from auth.schemas import JWTPayloadSchema
from config import settings


def encode_jwt(
    user: User,
    private_key: str = settings.JWT_PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
) -> str:
    payload = JWTPayloadSchema(
        sub=user.username,
        exp=datetime.utcnow() + timedelta(minutes=settings.JWT_TOKEN_EXP_MINUTES),
        is_admin=user.is_admin,
    )
    payload = payload.model_dump()
    return jwt.encode(payload, private_key, algorithm)


def decode_jwt(
    token,
    public_key: str = settings.JWT_PUBLIC_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
):
    return jwt.decode(token, public_key, algorithm)
