# ========================================================
# models.py
#   - 역할 : DB 테이블 구조를 Python 클래스로 정의(ORM 모델)
#   - ex) 이 파일의 클래스 1개 == DB 테이블 1개
#            클래스의 속성 1개 == 테이블의 컬럼 1개
# ========================================================

from sqlalchemy import Integer, String, Boolean # 컬럼 타입 import
# Mapped: ORM에 의해 관리되는 컬럼
# mapped_column: 파이썬 클래스의 속성을 데이터베이스 컬럼으로 연결하는 역할
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base

# Todo 모델 정의
class Todo(Base):
    # DB에서 실제로 사용할 테이블 이름
    __tablename__ = 'todo'

    id: Mapped[int] = mapped_column(
        Integer,            # 컬럼 타입 : 정수
        primary_key=True,   # 기본키
        autoincrement=True, # 자동 증가(1, 2, 3, ...)
    )
    title: Mapped[str] = mapped_column(
        String(255),    # 컬럼 타입 : 최대 255자 문자열
        nullable=False, # 값 필수
    )
    is_done: Mapped[bool] = mapped_column(
        Boolean,        # 컬럼 타입 : Bool
        nullable=False,
        default=False,  # 기본값 : False > 생성 시 미완료 상태
    )