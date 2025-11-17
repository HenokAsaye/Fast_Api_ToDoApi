from datetime import datetime, timedelta
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from todo_application.app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oAuth2Scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_password_hash(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str) -> bool:
    return pwd_context.verify(plain_password,hashed_password)
def create_access_token(subject:str,expires_delta:Optional[timedelta] = None) -> str:
    settings = get_settings()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub":subject,"exp":expire}
    return jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)

def decode_token(token:str) -> str:
    settings = get_settings()
    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        return payload.get("sub") or ""
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
def get_current_user(token:str = Depends(oAuth2Scheme)) -> str:
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
    return user_id