from sqlalchemy import Column, Integer, String, Text, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
import uuid


# Chatroom 모델
class Chatroom(Base):
    __tablename__ = "chatroom"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    user_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="chatroom_users")

# User 모델
class User(Base):
    __tablename__ = "user"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    
# Qna 모델
class Qna(Base):
    __tablename__ = "qna"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    references = Column(ARRAY(Text), nullable=False)
    create_date = Column(DateTime, nullable=False)
    chatroom_id = Column(UUID, ForeignKey("chatroom.id"))
    chatroom = relationship("Chatroom", backref="qnas")
    user_id = Column(UUID, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="qna_users")
    nexts = Column(ARRAY(Text))
