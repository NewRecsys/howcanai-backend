from models import Qna
from sqlalchemy.orm import Session

def get_qna_list(db: Session):
    qna_list = db.query(Qna).order_by(Qna.create_date.desc()).all()
    return qna_list