from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from domain.chatroom import chatroom_schema, chatroom_crud
from domain.user.user_router import get_current_user
from models import User
from starlette import status

router = APIRouter(
    prefix="/api/chatroom",
)

@router.get("/list", response_model = List[chatroom_schema.Chatroom])
def chatroom_list(db: Session = Depends(get_db)):
    _chatroom_list = chatroom_crud.get_chatroom_list(db)
    return _chatroom_list

@router.get("/detail/{chatroom_id}", response_model=chatroom_schema.Chatroom)
def chatroom_detail(chatroom_id: int, db: Session = Depends(get_db)):
    chatroom = chatroom_crud.get_chatroom(db, chatroom_id=chatroom_id)
    return chatroom


# @router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
# def chatroom_create(_chatroom_create: chatroom_schema.ChatroomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     chatroom_crud.create_chatroom(db=db, chatroom_create=_chatroom_create, user=current_user)

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def chatroom_create(_chatroom_create: chatroom_schema.ChatroomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chatroom_crud.create_chatroom(db=db, chatroom_create=_chatroom_create, user=current_user)

