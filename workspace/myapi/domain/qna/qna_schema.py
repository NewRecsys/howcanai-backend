import datetime

from pydantic import BaseModel

# Qna 스키마
class Qna(BaseModel):
    id: int
    user_id: int
    question: str
    answer: str
    referneces: list = []
    create_date: datetime.datetime
    
    # Qna 모델의 항목들이 자동으로 Qna 스키마로 매핑 됨
    class Config:
        from_attributes = True