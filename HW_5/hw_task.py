from fastapi import FastAPI, Request, Form
from typing import Optional
from pydantic import BaseModel
import uvicorn
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))

class User_data(BaseModel):
    name: str
    email: str
    password: str

class User(User_data):
    id: int

users = [
        User(id=1, name="Alex", email="alex@mail.ru", password="12345"),
        User(id=2, name="Oleg", email="oleg@mail.ru", password="qwerty"),
        ]

@app.get("/", response_model=list[User])
async def read_users():
    return users


@app.get("/users/", response_class=HTMLResponse, summary='список пользователей', tags=['пользователи'])
async def get_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})


@app.post('/users/', summary='Добавление нового пользователя (форма)', tags=['Добавить'])
async def add_new_user(request: Request, name=Form(), email=Form(), password=Form()):
    id = users[-1].id + 1
    user = User(id=id, name=name, email=email, password=password)
    users.append(user)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.post("/user/", response_model=User)
async def add_user(item: User_data):
    id = users[-1].id + 1
    user = User(id=id, name=item.name, email=item.email, password=item.password)
    users.append(user)
    return user

@app.get("/user/{id}", response_model=User)
async def get_user_id(id: int):
    for user in users:
        if user.id == id:
            return user
        
@app.put("/user/{id}", response_model=User)
async def put_user_id(id: int, new_data: User_data):
    for user in users:
        if user.id == id:
            user.name = new_data.name
            user.email = new_data.email
            user.password = new_data.password
            return user
    raise HTTPException(status_code=404, detail="Task not found")
        
@app.delete("/user/{id}")
async def del_user(id: int):
    for user in users:
        if user.id == id:
            users.remove(user)
            return users
    raise HTTPException(status_code=404, detail="Task not found")

if __name__ == '__main__':
    uvicorn.run(
        "hw_task:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )