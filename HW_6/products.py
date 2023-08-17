from fastapi import Form, Path, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from fastapi import Request
from db import *
from fastapi.templating import Jinja2Templates
from models import InputProducts, Products

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Создание нового продукта
@router.post("/product/add/", description="Добавить Продукт")
async def add_product(name_product: str = Form(...), description: str = Form(...), price: float = Form(...,gt=0, le=10000)):
    query = products_db.insert().values(
        name_product=name_product,
        description=description,
        price=price
    )
    await db.execute(query)
    return {"message": "Product added"}


# Просмотр продукта
@router.post("/product/{product_id}", description="Просмотреть продукт", response_model=Products)
async def viev_product(product_id: int):
    query = products_db.select().where( products_db.c.id == product_id)
    pr = await db.fetch_one(query)
    if not pr:
        raise HTTPException(status_code=404, detail="product not found")
    return pr


# Редактирование продукта
@router.put("/product/update/{product_id}")
async def update_product(product_id: int, product: InputProducts):
    query = products_db.update()\
        .where(products_db.c.id == product_id)\
        .values(**product.model_dump())
    await db.execute(query)
    return {"message": "product updated"}


# списко продуктов
@router.get("/products/", response_model=list[Products], description="Просмотреть все товары")
async def read_goods():
    query = products_db.select()
    return await db.fetch_all(query)

# Удаление товара
@router.delete("/product/del/{goods_id}", description="Удалить товар")
async def delete_goods(product_id: int):
    query = products_db.delete().where(products_db.c.id == product_id)
    await db.execute(query)
    return {'message': 'product deleted'}


@router.get("/products/orders/{product_id}")
async def get_product_orders(product_id: int = Path(..., title="Goods ID")):
    query = orders_db.select().where(orders_db.c.product_id == product_id)
    product_orders = await db.fetch_all(query)
    if not product_orders:
        raise HTTPException(status_code=404, detail="orders this product not found")
    return product_orders