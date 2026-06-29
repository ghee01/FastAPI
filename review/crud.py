# =========================================================
# review/crud.py
#   2026-06-29
#   DB 조작 함수
# 
#   CRUD : 데이터를 다루는 4가지 기본 동작
#       - Create    : 생성 POST(FastAPI) INSERT(SQL)
#       - Read      : 조회 GET(FastAPI) SELECT(SQL)
#       - Update    : 수정 PUT/PATCH(FastAPI) UPDATE(SQL)
#       - Delete    : 삭제 DELETE(FastAPI) / DELETE(SQL)
# ========================================================

from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import models, schemas

pwd_hasher = PasswordHash.recommended() # pwdlib이 권장하는 해싱 알고리즘(argon2) 자동 선택

# User CRUD
def get_user(db: Session, user_id: int):
    pass