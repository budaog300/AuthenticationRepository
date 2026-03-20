from fastapi import APIRouter, HTTPException, Response, Request
from src.core.security import SessionDep, UserDep, AdminUserDep
from src.users.schemas import UpdateUserSchema, AdminUpdateUserSchema, UserSchema, UserFullSchema
import src.users.crud as crud


router = APIRouter(prefix="/api/v1/users", tags=["Пользователи"])


@router.get("/profile", summary="Профиль")
async def get_profile(
        user: UserDep        
    ) -> UserSchema:
    return user


@router.patch("/profile", summary="Обновить данные профиля")
async def update_profile(
        update_data: UpdateUserSchema,
        user: UserDep,
        db: SessionDep
    ) -> UserSchema:
    return await crud.update_profile(update_data, user, db)


@router.delete("/profile", summary="Удалить свой аккаунт")
async def delete_profile(
    response: Response,
    user: UserDep,
    db: SessionDep
):
    await crud.delete_profile(user, db)
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return {"message": "Вы удалили свой профиль"}
    

@router.get("/", summary="Все пользователи (Админ)")
async def get_users(user: AdminUserDep, db: SessionDep) -> list[UserFullSchema]:
    return await crud.get_users_by_admin(db)


@router.patch("/{user_id}", summary="Изменить данные пользователя (Админ)")
async def update_user(
        user_id: int,
        update_data: AdminUpdateUserSchema,
        user: AdminUserDep,
        db: SessionDep
    ) -> UserFullSchema:
    return await crud.update_user_by_admin(user_id, update_data, db)