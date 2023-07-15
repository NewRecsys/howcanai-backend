from datetime import datetime

from domain.chatroom.chatroom_schema import ChatroomCreate

from models import Chatroom, User
from sqlalchemy.orm import Session

def get_chatroom_list(db: Session):
    chatroom_list = db.query(Chatroom).order_by(Chatroom.create_date.desc()).all()
    return chatroom_list

def get_chatroom(db: Session, chatroom_id: int):
    chatroom = db.query(Chatroom).get(chatroom_id)
    return chatroom

# def create_chatroom(db: Session, chatroom_create: ChatroomCreate, user: User):
#     db_chatroom = Chatroom(title=chatroom_create.title,
#                            create_date=datetime.now(),
#                            user=user,
#                            )
#     db.add(db_chatroom)
#     db.commit()

def create_chatroom(db: Session, chatroom_create: ChatroomCreate, user: User = None):
    db_chatroom = Chatroom(title=chatroom_create.title,
                           create_date=datetime.now(),
                           user=user,
                           )
    db.add(db_chatroom)
    db.commit()


    
    