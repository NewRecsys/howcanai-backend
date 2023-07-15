from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Chatroom 모델
class Chatroom(Base):
    __tablename__ = "chatroom"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="chatroom_users")

# User 모델
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    
# Qna 모델
class Qna(Base):
    __tablename__ = "qna"
    
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    references = Column(ARRAY(Text), nullable=False)
    create_date = Column(DateTime, nullable=False)
    chatroom_id = Column(Integer, ForeignKey("chatroom.id"))
    chatroom = relationship("Chatroom", backref="qnas")
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="qna_users")
