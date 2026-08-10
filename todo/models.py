# =================================================================================
# models.py
#   - SQLAlchemy ORM 모델 정의 파일
#   - 파이썬 클래스 ↔ DB 테이블 --> 매핑(mapping)하는 부분
#   - Todo 1개는 User 1명에게 속할 수 있다 --> 1:N
# 
# 기본키(PK)
#   - 테이블에서 각 행을 고유하게 식별하기 위한 컬럼
#   - 중복 불가
#   - 값 필수
#   - 테이블 내부에서 데이터를 구분하기 위한 기준

# 외래키(FK)
#   - 다른 테이블의 기본키를 참조하는 컬럼
#   - 한 테이블의 데이터가 다른 테이블의 어떤 데이터와 연결되었는지를 표현하기 위해 사용
#   - ex) 각 할 일이 어떤 사용자에게 속하는지 알 수 있다
#   - 테이블과 테이블 사이 관계를 표현하기 위한 연결 고리
# ==================================================================================

from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.orm import Base

# --- Todo 모델(할 일 테이블) ---
class Todo(Base):
    __tablename__ = 'todo'  # 실제 DB에 생성할 테이블 이름

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),   # user 테이블의 id 컬럼 참조
        nullable=True
    )

    # 관계 설정 - todo.user로 연결된 User 객체에 바로 접근 가능
    user: Mapped['User'] = relationship(
        back_populates='todos', # User쪽의 todos 속성과 서로 짝지어진다(양방향 관계)
    )


# --- User 모델(회원 테이블) ---
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,    # 중복 불가
        index=True,     # 검색 속도 향상
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False  # 비밀번호 - 평문X, '해시된 값'으로 저장
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),   # 행이 추가되는 시점에 자동으로 현재 시간 저장
        nullable=False
    )

    # 한 명의 회원은 여러 개의 todo를 가질 수 있다(리스트로 표현)
    todos: Mapped[list['Todo']] = relationship(
        back_populates='user',  # Todo 모델의 user 속성과 양방향으로 연결
        # all --> 추가(add), 삭제(delete), 병합(merge) 등 대부분의 동작을 부모(User)에서 자식(Todo)으로 연쇄적으로 적용
        cascade='all, delete-orphan'    # 회원 삭제 시, 그 회원의 todo 자동 삭제
    )