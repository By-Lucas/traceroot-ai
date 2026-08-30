from datetime import UTC, datetime, timedelta
from typing import Any, Literal

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import User, Workspace
from app.schemas.auth import RegisterRequest, TokenPair

password_hash = PasswordHash.recommended()
settings = get_settings()


def create_user(db: Session, payload: RegisterRequest) -> tuple[User, Workspace]:
    if db.scalar(select(User).where(User.email == payload.email.lower())):
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    user = User(
        email=payload.email.lower(),
        display_name=payload.display_name.strip(),
        password_hash=password_hash.hash(payload.password),
    )
    workspace = Workspace(name=f"{payload.display_name.strip()}'s workspace", owner=user)
    db.add_all([user, workspace])
    db.commit()
    db.refresh(user)
    db.refresh(workspace)
    return user, workspace


def authenticate(db: Session, email: str, password: str) -> User:
    user = db.scalar(select(User).where(User.email == email.lower()))
    if not user or not password_hash.verify(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")
    return user


def _encode(user: User, token_type: Literal["access", "refresh"], expires: timedelta) -> str:
    now = datetime.now(UTC)
    claims: dict[str, Any] = {
        "sub": user.id,
        "type": token_type,
        "iat": now,
        "exp": now + expires,
        "jti": __import__("uuid").uuid4().hex,
    }
    encoded = jwt.encode(claims, settings.secret_key, algorithm="HS256")
    return encoded.decode("utf-8") if isinstance(encoded, bytes) else encoded


def issue_tokens(user: User) -> TokenPair:
    return TokenPair(
        access_token=_encode(user, "access", timedelta(minutes=settings.access_token_minutes)),
        refresh_token=_encode(user, "refresh", timedelta(days=settings.refresh_token_days)),
    )


def decode_token(token: str, expected_type: Literal["access", "refresh"]) -> str:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        if payload.get("type") != expected_type or not payload.get("sub"):
            raise jwt.InvalidTokenError("wrong token type")
        return str(payload["sub"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from exc
