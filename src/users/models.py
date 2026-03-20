from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from src.core.database import Default, str_unique
from src.modules.models import Post

if TYPE_CHECKING:
    from src.modules.models import Post


class User(Default):
    __tablename__ = "users"

    username: Mapped[str_unique]
    email: Mapped[str_unique]
    password: Mapped[str]
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)

    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")   