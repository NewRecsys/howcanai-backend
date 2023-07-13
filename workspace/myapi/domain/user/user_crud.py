from passlib.context import CryptContext
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user_create: UserCreate):
    db_user = User(username=user_create.username,
                   password=pwd_context.hash(user_create.password),
                   email=user_create.email)
    db.add(db_user)
    db.commit()

# 입력 항목 중 사용자명 또는 이메일 값이 이미 존재하는지 확인
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
    (User.username == user_create.username) | (User.email == user_create.email)
    ).first()

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()