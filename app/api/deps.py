from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,SecurityScopes
from pydantic import ValidationError
from typing import List
from jose import JWTError
from sqlalchemy.orm import Session
from app.db.session import get_db
from ..core import security
from .. import crud, models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    authenticate_value = f'Bearer scope="{security_scopes.scope_str}"' if security_scopes.scopes else "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    payload = security.decode_hash_token(token)
    if not payload or payload.get("type") != "access":
        raise credentials_exception

    username = payload.get("sub")
    if not username:
        raise credentials_exception

    user = crud.crud_user.get_by_username(db, username)
    if not user:
        raise credentials_exception

    token_scopes = payload.get("scope", "").split()
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(status_code=403, detail="Not enough permissions")

    return user

def get_current_active_user(current_user: models.user.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
    

def scopes_for_role(role: str) -> List[str]:
    mapping = {
        "admin": ["me", "admin", "delete"],
        "user": ["me"],
    }
    return mapping.get(role, [])