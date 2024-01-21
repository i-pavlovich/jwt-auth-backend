from datetime import datetime, timedelta, timezone
from typing import Any

import jwt

from auth.models import RefreshToken, User
from auth.schemas import JWTPayloadSchema
from config import settings


def encode_jwt(
    user: User,
    exp_delta: timedelta = timedelta(minutes=settings.JWT_TOKEN_EXP_MINUTES),
    private_key: str = settings.JWT_PRIVATE_KEY_PATH.read_text(),
    algorithm: str = settings.ALGORITHM,
) -> str:
    payload = JWTPayloadSchema(
        sub=user.username,
        exp=datetime.utcnow() + exp_delta,
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


def get_refresh_token_cookie_settings(
    refresh_token: RefreshToken,
) -> dict[str, Any]:
    return {
        "key": settings.REFRESH_TOKEN_COOKIE_KEY,
        "value": refresh_token.value,
        "httponly": True,
        "secure": True,
        "samesite": "strict",
        "domain": settings.SITE_DOMAIN,
        "expires": refresh_token.expires_at.replace(tzinfo=timezone.utc),
    }
