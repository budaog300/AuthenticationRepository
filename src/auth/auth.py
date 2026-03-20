from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, or_, and_
from src.auth.schemas import AddUserSchema, LoginUserSchema
from src.users.models import User
from src.exceptions import ItemAlreadyExistException, UnauthorizedException


pwd_hash = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_hash.hash(password)


def verify_password(password: str, hash_password: str) -> bool:
    return pwd_hash.verify(password, hash_password)


async def create_user(user_data: AddUserSchema, db: AsyncSession):    
    query = (
        select(User)
        .where(
            or_(
                User.username == user_data.username,
                User.email == user_data.email,
            )
        )
    )
    try:
        res = await db.execute(query)        
        result = res.scalars().first()
        print(result)
        if not result: 
            user = user_data.model_dump(exclude={"confirm_password"})
            user["password"] = get_password_hash(user["password"])
            new_user = User(**user)
            db.add(new_user)            
            await db.commit()
            await db.refresh(new_user)
            return new_user
        raise ItemAlreadyExistException("Пользователь с таким email или username уже существует")
    except Exception as e:
        await db.rollback()
        raise e
    

async def authenticate(user_data: LoginUserSchema, db: AsyncSession):
    query = (
        select(User)
        .where(
            and_(
                or_(
                    User.username == user_data.login,
                    User.email == user_data.login,
                ),
                User.is_active == True
            )
        )
    )
    try:
        res = await db.execute(query)
        user = res.scalar_one_or_none()        
        if not user or not verify_password(user_data.password, user.password):
            raise UnauthorizedException("Неверный логин или пароль!")
        return user
    except Exception as e:
        raise e
    