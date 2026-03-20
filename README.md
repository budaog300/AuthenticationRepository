Архитектура проекта и управление доступом
# 1. Схема базы данных
Проектирование выполнено на основе SQLAlchemy 2.0 с использованием асинхронного движка asyncpg.

## Создание миграций:
```bash
    alembic init -t async migrations # Создает структуру Alembic в папке migrations
    alembic revision --autogenerate -m "Inital revision" # Сравнивает модели и состяние БД, после чего генерирует скрипт миграции
    alembic upgrade head # Применяет все непримененные миграции
```

В файле env.py папки migrations добавить строки
```Python
    from src.core.database import DATABASE_URL, Base
    from src.users.models import *
    from src.modules.models import *

    config.set_main_option("sqlalchemy.url", DATABASE_URL) # добавить после config = context.config
    ...
    target_metadata = Base.metadata # изменить None на Base.metadata
```

Затем самостоятельно создайте пользователя в приложении, потом используйте скрипты для начального наполнения БД, которые находятся в файле sql_queries (там указан user_id=1 у всех постов).

## Схемы моделей:
### **User**:
* id: int (Primary Key)
* username: str (Unique, Index)
* email: str (Unique, Index)
* password: str
* first_name: str
* last_name: str
* is_admin: bool (Default: False)
* is_active: bool (Default: True)
* created_at: datetime
* updated_at: datetime

### **Post**:
* id: int (Primary Key)
* title: str (Index)
* content: str
* user_id: int (ForeignKey: users.id, ON DELETE SET NULL)
* category_id: int (ForeignKey: categories.id, ON DELETE CASCADE)
* created_at: datetime
* updated_at: datetime

### **Category**
* id: int (Primary Key)
* name: str (Unique, Index)
* created_at: datetime
* updated_at: datetime

# 2. Управление ограничениями доступа
В приложении реализована модель управления доступом на основе ролей (RBAC), где права пользователя определяются через зависимости FastAPI (UserDep, AdminUserDep) на основе JWT-токенов и состояния записи в базе данных: 
* роль Guest (нет токена) позволяет только чтение публичных постов и авторизацию
* роль User (is_active: true) дает права на управление своим профилем и создание контента
* роль Admin (is_admin: true) предоставляет полный доступ к управлению всеми пользователями и категориями
* для деактивированных пользователей (is_active: false) доступ к сервису полностью заблокирован.

## Матрица прав доступа к эндпоинтам
### 🔑 Авторизация
* POST /register — Guest: Регистрация с автоматической выдачей JWT-токенов.

* POST /login — Guest: Аутентификация (проверка пароля и статуса is_active) с автоматической выдачей JWT-токенов.

* POST /logout — Any: Удаление access и refresh токенов.

* POST /refresh — Any: Обновление access и refresh токенов.

### 👤 Пользователи
* GET /profile — User: Доступ к данным профиля.

* PATCH /profile — User: Обновление данных профиля.

* DELETE /profile — User: Самостоятельная деактивация аккаунта.

* GET / — Admin Only: Просмотр списка всех пользователей.

* PATCH /{user_id} — Admin Only: Смена ролей и изменение данных любого пользователя.

### 📝 Посты
* GET / — Public: Просмотр всех постов.

* POST / — User: Создание нового поста (ID автора берется из токена).

* DELETE /{post_id} — User/Admin: Удаление поста (требуется проверка авторства или права админа).

## 🏷 Категории
* POST / — Admin Only: Создание новых категорий.

* DELETE /{cat_id} — Admin Only: Удаление категорий и связанных с ними постов.

# 3. Логика безопасности
**Аутентификация**: При логине проверяется соответствие пароля и флаг is_active. Если пользователь деактивирован, вход запрещен (403 Forbidden).

**Валидация токена**: Каждый защищенный запрос проверяет access_token в куках.

**Мягкое удаление**: Метод DELETE /profile не удаляет строку из БД физически, а выставляет is_active = false, что сохраняет целостность данных для постов, созданных ранее.