from fastapi import FastAPI, APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
import uvicorn
from chat.run import run_chat
from chat.args import parse_args
import uuid

from typing import List
from pydantic import BaseModel, Field, EmailStr

from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory='./')

@app.get("/chat/")
def get_query_form(request: Request):
    return templates.TemplateResponse('query_form.html', context={'request': request})

@app.post("/chat/")
def input_query(query:str = Form(...)):
    args = parse_args()
    args.query = query
    answer = run_chat(args)
    return {"Question": query, "Answer": answer}

class Chat(BaseModel):
    chat_id: int = Field(title ="해당 채팅방의 고유한 ID")
    user_id: int = Field(1111, title ="해당 채팅방 사용자의 고유한 ID")
    query: str = Field(title ="해당 채팅방에서 사용자가 요청한 질문")
    answer: str = Field(title ="해당 채팅방에서 사용자가 요청한 질문에 대한 답변")
    references: List[str] = Field([], title ="answer를 도출할 때 모델이 참고한 Reference 링크")
    create_time: datetime = Field(title ="해당 채팅방이 생성된 시간")


#### 회원 가입

# # router = APIRouter()
# class User(BaseModel):
#     email: EmailStr
#     password: str = Field(min_lenght=4, max_length=20)
#     name: str = Field(min_lenght=2, max_length=7)

# users = {}

# @app.get("/signup")
# def get_signup_form(request: Request):
#     return templates.TemplateResponse('signup_form.html', context={'request': request})

# @app.post("/signup")
# def signup(email: str, password: str, name: str):
#     user = User(email=email, password=password, name=name)
#     users[user.id] = user
#     return {"message": "회원가입이 완료되었습니다."}


# @app.post("/login")




###

if __name__ == '__main__':
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)