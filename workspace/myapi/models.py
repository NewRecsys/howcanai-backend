from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

# Chatroom 모델
class Chatroom(Base):
    __tablename__ = "chatroom"
    
    id = Column(Integer, primary_key=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)

# User 모델
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    