from datetime import datetime
from uuid import UUID

from domain.chatroom.chatroom_schema import ChatroomCreate, ChatroomUpdate

from models import Chatroom, User
from sqlalchemy.orm import Session

def get_chatroom_list(db: Session):
    chatroom_list = db.query(Chatroom).order_by(Chatroom.create_date.desc()).all()
    return chatroom_list

def get_chatroom_list_user(db: Session, user_id: UUID):
    chatroom_list = db.query(Chatroom).filter(Chatroom.user_id == user_id).order_by(Chatroom.create_date.desc()).all()
    return chatroom_list

def get_chatroom(db: Session, chatroom_id: UUID):
    chatroom = db.query(Chatroom).get(chatroom_id)
    return chatroom


def create_chatroom(db: Session, chatroom_create: ChatroomCreate, user: User = None):
    db_chatroom = Chatroom(title=chatroom_create.title,
                           create_date=datetime.now(),
                           user=user,
                           )
    db.add(db_chatroom)
    db.commit()
    return db_chatroom.id

def update_chatroom(db: Session, db_chatroom: Chatroom, chatroom_update: ChatroomUpdate):
    db_chatroom.title = chatroom_update.title
    db.add(db_chatroom)
    db.commit()