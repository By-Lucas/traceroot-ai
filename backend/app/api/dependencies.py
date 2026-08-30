from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User, Workspace
from app.services.auth import decode_token

bearer = HTTPBearer(auto_error=False)
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
) -> User:
    if not credentials:
        raise HTTPException(status_code=401, detail="Authentication required")
    user_id = decode_token(credentials.credentials, "access")
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is unavailable")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def owned_workspace(db: Session, user: User) -> Workspace:
    workspace = db.scalar(select(Workspace).where(Workspace.owner_id == user.id))
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return workspace
