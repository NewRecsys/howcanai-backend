from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.chatroom import chatroom_schema, chatroom_crud

router = APIRouter(
    prefix="/api/chatroom",
)

@router.get("/list", response_model = List[chatroom_schema.Chatroom])
def chatroom_list(db: Session = Depends(get_db)):
    _chatroom_list = chatroom_crud.get_chatroom_list(db)
    return _chatroom_list