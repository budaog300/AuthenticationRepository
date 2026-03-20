from pydantic import BaseModel, Field, EmailStr
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from src.modules.schemas import PostSchema


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str    


class UserFullSchema(UserSchema):
    created_at: datetime
    updated_at: datetime
    is_admin: bool
    is_active: bool


class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=5, max_length=20, description="Изменить логин пользователя")
    email: Optional[EmailStr] = Field(None, min_length=5, description="Изменить Email пользователя")    
    first_name: Optional[str] = Field(None, min_length=5, description="Изменить имя пользователя")
    last_name: Optional[str] = Field(None, min_length=5, description="Изменить фамилию пользователя")


class AdminUpdateUserSchema(UpdateUserSchema):
    is_admin: Optional[bool] = Field(None, description="Изменить роль пользователя")
    is_active: Optional[bool] = Field(None, description="Изменить статус пользователя")


from src.modules.schemas import PostSchema
UserSchema.model_rebuild()