from pydantic import BaseModel, Field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.users.schemas import UserSchema


class PostSchema(BaseModel):
    title: str
    content: str


class PostFullSchema(PostSchema):
    category: "CategorySchema"
    user: "UserSchema"


class AddPostSchema(BaseModel):
    title: str = Field(..., min_length=5, max_length=30, description="Заголовок поста")
    content: str = Field(..., min_length=5, description="Контент поста")
    category_id: int


class CategorySchema(BaseModel):
    name: str    


class AddCategorySchema(BaseModel):
    name: str = Field(..., min_length=5, max_length=30, description="Название категории")


from src.users.schemas import UserSchema
PostSchema.model_rebuild()