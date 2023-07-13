import datetime

from pydantic import BaseModel

# Chatroom 스키마
class Chatroom(BaseModel):
    id: int
    question: str
    answer: str
    create_date: datetime.datetime
    
    # CharRoom 모델의 항목들이 자동으로 Chatroom 스키마로 매핑 됨
    class Config:
        from_attributes = True