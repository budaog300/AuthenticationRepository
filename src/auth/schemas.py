from pydantic import BaseModel, Field, EmailStr, model_validator


class AddUserSchema(BaseModel):
    username: str = Field(..., min_length=5, max_length=20, description="Введите логин пользователя")
    email: EmailStr = Field(..., min_length=5, description="Введите Email пользователя")
    password: str = Field(..., min_length=5, description="Введите пароль пользователя")
    confirm_password: str = Field(..., min_length=5, description="Повторите пароль")
    first_name: str = Field(..., min_length=3, description="Введите имя пользователя")
    last_name: str = Field(..., min_length=3, description="Введите фамилию пользователя")

    @model_validator(mode="after")
    def check_passwords_match(self) -> "AddUserSchema":
        if self.password != self.confirm_password:
            raise ValueError(["Пароли не совпадают!"])
        return self


class LoginUserSchema(BaseModel):
    login: str = Field(..., description="Введите почту или логин пользователя")    
    password: str = Field(..., description="Введите пользователя")