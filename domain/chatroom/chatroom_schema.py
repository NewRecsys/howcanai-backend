import datetime
from typing import List
from pydantic import BaseModel, validator

from domain.qna.qna_schema import Qna
from uuid import UUID

# Chatroom 스키마
class Chatroom(BaseModel):
    id: UUID
    title: str
    create_date: datetime.datetime
    qnas: List[Qna]
    
    # CharRoom 모델의 항목들이 자동으로 Chatroom 스키마로 매핑 됨
    class Config:
        orm_mode = True

class ChatroomList(BaseModel):
    id: UUID
    title: str
    create_date: datetime.datetime
    
    # CharRoom 모델의 항목들이 자동으로 Chatroom 스키마로 매핑 됨
    class Config:
        orm_mode = True

class ChatroomCreate(BaseModel):
    title: str = 'New Chat'
    
    @validator('title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class ChatroomUpdate(ChatroomCreate):
    chatroom_id: UUID
    
class ChatroomDelete(BaseModel):
    chatroom_id: UUID
    