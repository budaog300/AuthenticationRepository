from fastapi import APIRouter, HTTPException, Response, Request
from src.auth.auth import create_user, authenticate
from src.core.security import SessionDep, UserDep, generate_tokens, update_refresh_token
from src.auth.schemas import AddUserSchema, LoginUserSchema


router = APIRouter(prefix="/api/v1/auth", tags=["Авторизация"])


@router.post("/register", summary="Зарегистрироваться")
async def register(
        user_data: AddUserSchema, 
        response: Response, 
        db: SessionDep
    ):
    user = await create_user(user_data, db)    
    tokens = generate_tokens(response, {"sub": str(user.id)})
    return {"message": "Вы успешно зарегистрировались в системе", **tokens}


@router.post("/login", summary="Войти в систему")
async def login(
        user_data: LoginUserSchema, 
        response: Response, 
        db: SessionDep
    ):    
    user = await authenticate(user_data, db)    
    tokens = generate_tokens(response, {"sub": str(user.id)})
    return {"message": "Вы вошли в систему", **tokens}


@router.post("/logout", summary="Выйти из системы")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Вы вышли из системы"}


@router.post("/refresh", summary="Обновить Refresh токен")
async def refresh(
        request: Request, 
        response: Response, 
        db: SessionDep
    ):
    return await update_refresh_token(request, response, db)   