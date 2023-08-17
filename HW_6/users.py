from fastapi import Form, Path, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import Request
from db import *
from fastapi.templating import Jinja2Templates
from models import InputUser, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Создание нового пользователя
@router.post("/user/add/", description="Добавить Пользователя")
async def add_user(name: str = Form(...), surname: str = Form(...), email: str = Form(...),
                   password: str = Form(...)):
    query = users_db.insert().values(
        name=name,
        surname=surname,
        email=email,
        password=password
    )
    await db.execute(query)
    return {"message": "User added"}


# Просмотр одного пользователя
@router.post("/user/{user_id}", description="Просмотреть  Пользователя", response_model=User)
async def viev_user(user_id: int):
    query = users_db.select().where(users_db.c.id == user_id)
    us = await db.fetch_one(query)
    if not us:
        raise HTTPException(status_code=404, detail="User not found")
    return us


# Редактирование пользователя
@router.put("/user/update/{user_id}", description="Редактировать пользователя")
async def update_user(user_id: int, user: InputUser):
    query = users_db.update().where(users_db.c.id == user_id).values(**user.model_dump())
    await db.execute(query)
    return {"message": "User updated"}

# Список пользователей
@router.get("/users/", response_model=list[User], description="Просмотреть всех пользователей")
async def read_users():
    query = users_db.select()
    return await db.fetch_all(query)

# Удаление пользователя
@router.delete("/user/del/{user_id}", description="Удалить пользователя")
async def delete_user(user_id: int):
    query = users_db.delete().where(users_db.c.id == user_id)
    await db.execute(query)
    return {'message': 'User deleted'}


@router.get("/user/orders/{user_id}")
async def get_user_orders(user_id: int = Path(..., title="User ID")):
    query = orders_db.select().where(orders_db.c.user_id == user_id)
    user_orders = await db.fetch_all(query)
    if not user_orders:
        raise HTTPException(status_code=404, detail="User not found or has no orders")
    return user_orders