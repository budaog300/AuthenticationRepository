from sqlalchemy import select, insert, delete, update, or_, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.users.models import User
from src.modules.models import Post
from src.users.schemas import UpdateUserSchema, AdminUpdateUserSchema, UserSchema, UserFullSchema
from src.exceptions import BadRequestException, ItemNotFoundException


async def update_profile(user_data: UpdateUserSchema, user: User, db: AsyncSession) -> UserSchema:
    user_data_dict = user_data.model_dump(exclude_unset=True)
    if not user_data_dict:
        return user
    query = (
        select(User)
        .where(
            and_(
                or_(
                    User.username == user_data.username,
                    User.email == user_data.email,
                ),
                User.id != user.id
            )
        )
    )
    try:
        res = await db.execute(query)
        existing_user = res.scalars().first()
        if existing_user:
            raise BadRequestException("Пользователь с таким логином уже сущестует!")
        
        stmt = (
            update(User)
            .values(**user_data_dict)
            .where(User.id == user.id)
        )    
        await db.execute(stmt)        
        await db.commit()
        await db.refresh(user)
        return user        
    except SQLAlchemyError as e:
        await db.rollback()
        raise e


async def delete_profile(user: User, db: AsyncSession) -> UserSchema:
    user.is_active = False
    try:
        await db.commit()        
        return user
    except SQLAlchemyError as e:
        await db.rollback()
        raise e
    

async def get_users_by_admin(db: AsyncSession) -> list[UserFullSchema]:
    query = (
        select(User)
        .options(selectinload(User.posts))
    )
    try:
        users = await db.execute(query)
        return users.scalars().all()
    except SQLAlchemyError as e:       
        raise e


async def update_user_by_admin(user_id: int, user_data: AdminUpdateUserSchema, db: AsyncSession) -> UserFullSchema:
    user_data_dict = user_data.model_dump(exclude_unset=True)   
    if not user_data_dict:
        return await db.get(User, user_id)
    stmt = (
        update(User)
        .values(**user_data_dict)
        .where(User.id == user_id)
        .returning(User)
    )
    try:
        res = await db.execute(stmt)
        updated_user = res.scalar_one_or_none()
        if not updated_user:
            raise ItemNotFoundException("Пользователь не найден!")
        await db.commit()        
        return updated_user
    except SQLAlchemyError as e:
        await db.rollback()
        raise e