from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from domain.qna import qna_schema, qna_crud

router = APIRouter(
    prefix="/api/qna",
)

@router.get("/list", response_model = List[qna_schema.Qna])
def qna_list(db: Session = Depends(get_db)):
    _qna_list = qna_crud.get_qna(db)
    return _qna_list