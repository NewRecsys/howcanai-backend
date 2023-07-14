import datetime
from typing import List
from pydantic import BaseModel, validator

# Qna 스키마
class Qna(BaseModel):
    id: int
    question: str
    answer: str
    references: List[str]
    create_date: datetime.datetime
    
    # Qna 모델의 항목들이 자동으로 Qna 스키마로 매핑 됨
    class Config:
        orm_mode = True

class QnaCreate(BaseModel):
    query: str
    
    @validator('query')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v