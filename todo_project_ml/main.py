'''
todo_project/main.py

FastAPI 애플리케이션의 진입점 (entry point)
JWT 인증 토큰 방식 사용

- 앱 인스턴스를 만들고, 여러 개로 나뉜 라우터들을 하나로 조립하고,
  서버가 켜질 때/꺼질 때 딱 한 번씩 해야 하는 일(DB 테이블 생성, ML 모델 로드)을 처리한다
'''

from pathlib import Path
import joblib
from fastapi import FastAPI
from database.db_connection import engine
from database.orm import Base
from routers.todo import router as todo_router
from routers.user import router as user_router
from routers.ml import router as ml_router
from contextlib import asynccontextmanager

# 모델 경로
MODEL_PATH = Path(__file__).resolve().parent / 'ml' / 'artifacts' / 'latest.pkl'

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 시 1회 실행 : models.py에 정의된 테이블들을 DB에 생성
    # (이미 테이블이 있으면 아무 일도 하지 않는다)
    Base.metadata.create_all(bind=engine)

    # 카테고리 예측 ML 모델 로드
    # → 서버가 켜질 때 딱 한 번만 수행해서, app_state에 보관
    #   app_state : FastAPI가 기본 제공하는 앱 영역에서 공유하는 저장 공간
    if MODEL_PATH.exists():
        app.state.category_model = joblib.load(MODEL_PATH)
        print(f'[INFO] 카테고리 예측 모델 로드 완료 : {MODEL_PATH}')
    else:
        # 모델 파일이 없어도 서버가 안 켜지게 막지 않는다
        # 회원가입/로그인/Todo CRUD 는 ML과 무관하게 항상 정상 동작해야 하기 때문이다
        app.state.category_model = None
        print(f'[WARN] 모델 파일이 없습니다. ({MODEL_PATH}) 먼저 `python ml/train_model.py`를 실행하세요.')

    # FastAPI가 이제 요청을 받아도 좋다고 판단하고 실제 서비스 시작
    yield

# FastAPI 앱 객체 생성
# lifespan에 위에 만든 함수를 연결해서 "서버 켜질 때 테이블 자동 생성"이 실제로 작업
app = FastAPI(lifespan=lifespan)

# router/todo.py, router/user.py에서 만든 라우터를 app 하나에 "합체" 시키는 부분
app.include_router(todo_router)
app.include_router(user_router)
app.include_router(ml_router)