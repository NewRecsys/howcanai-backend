from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.chatroom import chatroom_schema, chatroom_crud
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


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def chatroom_create(_chatroom_create: chatroom_schema.ChatroomCreate, db: Session = Depends(get_db)):
    chatroom_crud.create_chatroom(db=db, chatroom_create=_chatroom_create)
    
