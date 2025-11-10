from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
# from passlib.context import CryptContext
from pwdlib import PasswordHash
from app.core.config import settings

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

password_hash = PasswordHash.recommended()


def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp':expires})

    return jwt.encode(to_encode,SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

def get_password_hash(password):
    return password_hash.hash(password)

def decode_hash_token(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None