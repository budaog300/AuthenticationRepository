from jose import jwt, JWTError
from fastapi import Depends, Response, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from typing import Annotated
from src.core.config import settings
from src.core.database import get_db
from src.users.models import User
from src.exceptions import ForbiddenException, UnauthorizedException


auth_data = settings.get_auth_data


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire, "type": "access"})    
    return jwt.encode(to_encode, key=auth_data["access_secret_key"], algorithm=auth_data["algorithm"])


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    auth_data = settings.get_auth_data
    return jwt.encode(to_encode, key=auth_data["refresh_secret_key"], algorithm=auth_data["algorithm"])


def generate_tokens(response: Response, data: dict):
    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return {"access_token": access_token, "refresh_token": refresh_token}


async def update_refresh_token(request: Request, response: Response, db: AsyncSession):
    token = request.cookies.get("refresh_token")
    if not token:
        raise UnauthorizedException("Требуется токен!")
    try:
        payload = jwt.decode(token, key=auth_data["refresh_secret_key"], algorithms=auth_data["algorithm"])
        if payload.get("type") != "refresh":
            raise UnauthorizedException("Неправильный тип токена!")
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Не найден ID пользователя!")
        query = (
            select(User)
            .where(User.id == int(user_id))
        )
        user = (await db.execute(query)).scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedException("Пользователь не найден!")        
        tokens = generate_tokens(response, {"sub": str(user_id)})
        return {"message":"Токен обновлен", "access_token": tokens["access_token"], "refresh_token": tokens["refresh_token"]}
    except JWTError:
        raise UnauthorizedException("Токен не валидный!")


async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise UnauthorizedException("Требуется токен!")
    try:
        payload = jwt.decode(token, key=auth_data["access_secret_key"], algorithms=auth_data["algorithm"])
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Не найден ID пользователя!")        
        query = (
            select(User)
            .where(User.id == int(user_id))
        )
        user = (await db.execute(query)).scalar_one_or_none()
        if not user or not user.is_active:
            raise UnauthorizedException("Пользователь не найден")
        return user
    except JWTError:
        raise UnauthorizedException("Токен не валидный!")


async def get_current_admin_user(user: User = Depends(get_current_user)):
    if not user.is_admin:
        raise ForbiddenException("Недостаточно прав!")
    return user


SessionDep = Annotated[AsyncSession, Depends(get_db)]
UserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(get_current_admin_user)]