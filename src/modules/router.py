from fastapi import APIRouter, HTTPException

from src.core.security import SessionDep, UserDep, AdminUserDep
from src.modules.schemas import AddPostSchema, PostSchema, PostFullSchema, AddCategorySchema, CategorySchema
import src.modules.crud as crud


post_router = APIRouter(prefix="/posts", tags=["Посты"])
category_router = APIRouter(prefix="/categories", tags=["Категории"])


@post_router.post("/", summary="Создать пост")
async def create_post(post: AddPostSchema, user: UserDep, db: SessionDep) -> PostSchema:
    return await crud.create_post(post, user, db)


@post_router.get("/", summary="Все посты")
async def get_posts(db: SessionDep) -> list[PostFullSchema]:
    return await crud.get_posts(db)


@post_router.delete("/{post_id}", summary="Удалить пост")
async def delete_post(post_id: int, user: UserDep, db: SessionDep):
    await crud.delete_post(post_id, user, db)    
    return {"message": "Пост успешно удален!"}


@category_router.post("/", summary="Создать категорию")
async def create_category(category: AddCategorySchema, user: AdminUserDep, db: SessionDep) -> CategorySchema:
    return await crud.create_category(category, db)


@category_router.delete("/{cat_id}", summary="Удалить категорию")
async def delete_category(cat_id: int, user: AdminUserDep, db: SessionDep):
    await crud.delete_category(cat_id, db)    
    return {"message": "Категория успешно удалена!"}


router = APIRouter(prefix="/api/v1")
router.include_router(post_router)
router.include_router(category_router)