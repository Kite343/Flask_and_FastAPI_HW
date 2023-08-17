import datetime
from pydantic import BaseModel, Field
from typing import Optional

class InputUser(BaseModel):
    name: str = Field(title="name", min_length=2)
    surname: str = Field(title="surname", min_length=2)
    email: str = Field(title="email", min_length=5)
    password: str = Field(title="password", min_length=5)


class User(InputUser):
    id: int

class InputProducts(BaseModel):
    name_product: str = Field(title="name_product", min_length=2)
    description: str = Field(title="description", min_length=2)
    price: float = Field(title="price", gt=0)

class Products(InputProducts):
    id: int


class InputOrder(BaseModel):
    user_id: int
    product_id: int
    date: Optional[datetime.datetime] = datetime.datetime.now
    order_status: str


class Order(InputOrder):
    id: int