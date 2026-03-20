from sqlalchemy import select, insert, delete, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.modules.models import Post, Category
from src.users.models import User
from src.modules.schemas import AddPostSchema, PostSchema, PostFullSchema, AddCategorySchema, CategorySchema
from src.exceptions import ItemNotFoundException, ForbiddenException


async def create_post(data: AddPostSchema, user: User, db: AsyncSession) -> PostSchema:   
    new_post = Post(**data.model_dump(), user_id=user.id)
    db.add(new_post)
    try:        
        await db.commit()
        await db.refresh(new_post)
        return new_post
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    

async def get_posts(db: AsyncSession) -> list[PostFullSchema]:
    query = (
        select(Post)
        .options(joinedload(Post.category), joinedload(Post.user))
    )
    try:        
        posts = await db.execute(query)
        return posts.scalars().all()
    except SQLAlchemyError as e:        
        raise e


async def delete_post(post_id: int, user: User, db: AsyncSession) -> bool:
    post = await db.get(Post, post_id)
    if not post:
        raise ItemNotFoundException("Пост не найден")
    if post.user_id != user.id and not user.is_admin:
        raise ForbiddenException("Вы не можете удалять чужой контент")
    try:  
        await db.delete(post)
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    

async def create_category(category: AddCategorySchema, db: AsyncSession) -> CategorySchema:
    new_category = Category(**category.model_dump())
    db.add(new_category)
    try:
        await db.commit()
        await db.refresh(new_category)
        return new_category
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    

async def delete_category(cat_id: int, db: AsyncSession) -> bool:
    stmt = delete(Category).where(Category.id == cat_id)
    try:
        result = await db.execute(stmt)
        if result.rowcount == 0:
            raise ItemNotFoundException("Категория не найдена")
        await db.commit()
        return True
    except SQLAlchemyError as e:
        await db.rollback()
        raise e