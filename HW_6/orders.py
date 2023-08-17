from fastapi import Form, Path, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import Request
from db import *
from fastapi.templating import Jinja2Templates
from models import InputOrder, Order
from typing import Optional
import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# добавление сделки
@router.post("/order/add/")
async def add_order(user_id: int = Form(...), product_id: int = Form(...), order_status: str = Form(...), date: Optional[datetime.datetime] = Form(default=datetime.datetime.now())):
    query = orders_db.insert().values(
        user_id=user_id,
        product_id=product_id,
        date = date,
        order_status=order_status
    )
    await db.execute(query)
    return {"message": "Order added"}

# добавление сделки
# @router.post("/order/add/")
# async def add_order(order: InputOrder):
#     query = orders_db.insert().values(**order.model_dump())
#     await db.execute(query)
#     return {"message": "Order added"}

# Редактирование сделки
@router.put("/order/update/{order_id}", description="Редактировать сделку")
async def update_order(order_id: int, order: InputOrder):
    query = orders_db.update().where(orders_db.c.id == order_id).values(**order.model_dump())
    await db.execute(query)
    return {"message": "order updated"}

# Список сделок
@router.get("/orders/", response_model=list[Order], description="Просмотреть все сделки")
async def read_orders():
    query = orders_db.select()
    return await db.fetch_all(query)

# Удаление сделки
@router.delete("/order/del/{order_id}", description="Удалить сделку")
async def delete_user(order_id: int):
    query = orders_db.delete().where(orders_db.c.id == order_id)
    await db.execute(query)
    return {'message': 'order deleted'}

