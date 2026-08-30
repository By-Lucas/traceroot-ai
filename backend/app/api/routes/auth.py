from fastapi import APIRouter, HTTPException

from app.api.dependencies import CurrentUser, DbSession, owned_workspace
from app.models import User
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenPair, UserResponse
from app.services.auth import authenticate, create_user, decode_token, issue_tokens

router = APIRouter(prefix="/auth", tags=["authentication"])


def response_for(user: User, workspace_id: str) -> UserResponse:
    return UserResponse(
        id=user.id, email=user.email, display_name=user.display_name, workspace_id=workspace_id
    )


@router.post("/register", response_model=TokenPair, status_code=201)
def register(payload: RegisterRequest, db: DbSession) -> TokenPair:
    user, _ = create_user(db, payload)
    return issue_tokens(user)


@router.post("/login", response_model=TokenPair)
def login(payload: LoginRequest, db: DbSession) -> TokenPair:
    return issue_tokens(authenticate(db, payload.email, payload.password))


@router.post("/refresh", response_model=TokenPair)
def refresh(payload: RefreshRequest, db: DbSession) -> TokenPair:
    user_id = decode_token(payload.refresh_token, "refresh")
    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User is unavailable")
    return issue_tokens(user)


@router.get("/me", response_model=UserResponse)
def me(user: CurrentUser, db: DbSession) -> UserResponse:
    workspace = owned_workspace(db, user)
    return response_for(user, workspace.id)


@router.post("/logout", status_code=204)
def logout(_: CurrentUser) -> None:
    # Access tokens are intentionally short-lived; clients discard both tokens.
    return None
