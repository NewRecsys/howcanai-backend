from models import Chatroom
from sqlalchemy.orm import Session

def get_chatroom_list(db: Session):
    chatroom_list = db.query(Chatroom).order_by(Chatroom.create_date.desc()).all()
    return chatroom_list