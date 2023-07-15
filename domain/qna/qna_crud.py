from models import Qna, Chatroom, User
from domain.qna.qna_schema import QnaCreate
from sqlalchemy.orm import Session
from chat.run import run_chat
from datetime import datetime
from chat.args import parse_args

args = parse_args()


def get_qna_list(db: Session):
    qna_list = db.query(Qna).order_by(Qna.create_date.desc()).all()
    return qna_list



def create_qna(db: Session, chatroom: Chatroom, qna_create: QnaCreate, user: User):
    answer_, references_ = run_chat(args, query = qna_create.query)
    db_qna = Qna(
        question=qna_create.query,
        answer=answer_,
        references=references_,
        create_date=datetime.now(),
        chatroom=chatroom,
        user=user,
    )
    db.add(db_qna)
    db.commit()
    
    