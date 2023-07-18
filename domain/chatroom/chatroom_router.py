from fastapi import APIRouter, Depends, HTTPException
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

# @router.get("/list", response_model = List[chatroom_schema.Chatroom])
# def chatroom_list(db: Session = Depends(get_db)):
#     _chatroom_list = chatroom_crud.get_chatroom_list(db)
#     return _chatroom_list


@router.get("/list", response_model = List[chatroom_schema.Chatroom])
def chatroom_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    _chatroom_list = chatroom_crud.get_chatroom_list_user(db, current_user.id)
    return _chatroom_list

@router.get("/detail/{chatroom_id}", response_model=chatroom_schema.Chatroom)
def chatroom_detail(chatroom_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chatroom = chatroom_crud.get_chatroom(db, chatroom_id=chatroom_id)
    if current_user.id != chatroom.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="현재 로그인된 유저가 접근할 수 없는 채팅방입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return chatroom

@router.post("/create")
def chatroom_create(_chatroom_create: chatroom_schema.ChatroomCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    chatroom_id = chatroom_crud.create_chatroom(db=db, chatroom_create=_chatroom_create, user=current_user)
    return { 'chatroom_id' : chatroom_id }

# @router.get("/list/{user_id}", response_model = List[chatroom_schema.Chatroom])
# def chatroom_list_user(user_id: int, db: Session = Depends(get_db)):
#     _chatroom_list = chatroom_crud.get_chatroom_list_user(db, user_id)
#     return _chatroom_list

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def chatroom_update(_chatroom_update: chatroom_schema.ChatroomUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_chatroom = chatroom_crud.get_chatroom(db, chatroom_id=_chatroom_update.chatroom_id)
     
    # 로그인한 사용자만 가능하게 설정하기
    if current_user.id != db_chatroom.user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="현재 로그인된 유저가 접근할 수 없는 채팅방입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not db_chatroom:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    
   
    chatroom_crud.update_chatroom(db=db, db_chatroom=db_chatroom, chatroom_update=_chatroom_update)
    