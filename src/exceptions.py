from fastapi import HTTPException


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):        
        super().__init__(status_code=status_code, detail=detail)


class BadRequestException(CustomException):
    def __init__(self, detail: str = "Плохой запрос"):        
        super().__init__(detail, 400)


class UnauthorizedException(CustomException):
    def __init__(self, detail: str = "Пользователь не авторизован!"):
        super().__init__(detail, 401)


class ForbiddenException(CustomException):
    def __init__(self, detail: str = "Доступ запрещен!"):
        super().__init__(detail, 403)


class ItemNotFoundException(CustomException):
    def __init__(self, detail: str = "Элемент не найден!"):
        super().__init__(detail, 404)
        

class ItemAlreadyExistException(CustomException):
    def __init__(self, detail: str = "Пользователь уже существует!"):
        super().__init__(detail, 409)       