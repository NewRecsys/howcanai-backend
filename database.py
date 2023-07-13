from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

# create_engine: 커넥션 풀을 생성, 데이터베이스에 접속하는 객체를 일정 갯수만큼 만들어 놓고 돌려가며 사용하는 것
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 데이터베이스 접속을 위한 클래스
# autocommit=False: 데이터를 변경했을 때 commit이라는 사인을 주어야만 실제 저장이 됨, 데이터를 잘못 저장했을 경우 rollback 사인으로 되돌리는 것이 가능
# autocommit=True: commit이라는 사인이 없어도 즉시 데이터베이스에 변경사항이 적용, commit이 필요없는 것처럼 rollback도 동작하지 않는다는 점에 주의
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bse: 데이터베이스 모델을 구성할 때 사용되는 클래스
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()