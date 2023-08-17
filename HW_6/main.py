import uvicorn
from db import *
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import users
import orders
import products


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.include_router(users.router, tags=['Пользователи'])
app.include_router(products.router, tags=['Товары'])
app.include_router(orders.router, tags=['Заказы'])


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )