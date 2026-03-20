from sqlalchemy import text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from src.core.database import Default, str_unique

if TYPE_CHECKING:
    from src.users.models import User


class Post(Default):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    user: Mapped["User"] = relationship("User", back_populates="posts")

    __table_args__ = (
        Index("TitleIndex", "title"),
    )


class Category(Default):
    __tablename__ = "categories"

    name: Mapped[str_unique]
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")

    __table_args__ = (
        Index("CategoryNameIndex", "name"),
    )