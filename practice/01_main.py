# FastAPI 클래스 불러오기
from fastapi import FastAPI

app = FastAPI()

# 서버 실행
@app.get('/') # / 경로로 GET요청이 오면 아래 함수 실행하라는 데코레이터
def root_handler():
    # 딕셔너리 반환 시, FastAPI가 자동으로 JSON으로 변환해서 응답
    return {'message':'Hello, FastAPI!'}