from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import text
from typing import Annotated
from datetime import datetime
from src.core.config import settings


DATABASE_URL = settings.get_url_db
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, unique=True)]
str_unique = Annotated[str, mapped_column(unique=True, nullable=False)]


class Base(DeclarativeBase):
    __abstract__ = True

   
class Default(Base):
    __abstract__ = True

    id: Mapped[int_pk]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))


async def get_db():
    async with async_session() as session:
        yield session    