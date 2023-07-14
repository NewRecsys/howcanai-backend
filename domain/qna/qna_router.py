from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.qna import qna_schema, qna_crud
from domain.chatroom import chatroom_crud
from starlette import status


router = APIRouter(
    prefix="/api/qna",
)

@router.get("/list", response_model = List[qna_schema.Qna])
def qna_list(db: Session = Depends(get_db)):
    _qna_list = qna_crud.get_qna_list(db)
    return _qna_list


@router.post("/create/{chatroom_id}", status_code=status.HTTP_204_NO_CONTENT)
def qna_create(chatroom_id: int, _qna_create: qna_schema.QnaCreate, db: Session = Depends(get_db)):
    chatroom = chatroom_crud.get_chatroom(db, chatroom_id=chatroom_id)
    if not chatroom:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    qna_crud.create_qna(db=db, chatroom=chatroom, qna_create=_qna_create)