# ========================================================
# main.py
#   - 역할 : FastAPI 앱 정의 + CRUD 라우터 5개
# 
# API 목록
#   - GET       /todos              : 전체 할 일 조회
#   - GET       /todos/{todo_id}    : 단일 할 일 조회
#   - POST      /toods              : 할 일 생성
#   - PATCH     /todos/{todo_id}    : 할 일 수정
#   - DELETE    /todos/{todo_id}    : 할 일 삭제
# ========================================================

from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import select   # ORM 모델을 기준으로 조회 쿼리 객체를 생성
from database.db_connection import engine, SessionFactory
from database.orm import Base
from models import Todo

# 앱 시작 시 테이블 자동 생성
#   Base를 상속받은 모든 모델(Todo 등)의 테이블을 DB에 자동 생성
#   이미 테이블이 있으면 건너뜀(데이터 삭제 X)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# GET  /todos
@app.get(
    '/todos',
    response_model=list[TodoResponse],
    status_code=status.HTTP_200_OK
)
def get_todos_handler():
    session = SessionFactory()
    try:
        # stmt : SQL문을 의미하는 statement의 약자
        stmt = select(Todo) # 데이터 조회 쿼리 객체(아직 데이터베이스에는 접근 하지 않았다)
        # session.execute(stmt) : 쿼리 객체를 실제 데이터베이스에 전달해서 실행
        # .scalars().all() : 실행 결과에서 테이블의 각 행에 대응되는 ORM 객체 추출 > 리스트
        todos = session.execute(stmt).scalars().all()   # 전체 결과 리스트로 반환
        return todos
    finally:
        session.close()

# GET  /todos/{todo_id}
@app.get(
    '/todos/{todo_id}',
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def get_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()  # 첫 번째 결과 1개 저장
        if todo:
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    finally:
        session.close()

# POST  /todos
@app.post(
    '/todos',
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_todo_handler(body: TodoCreateRequest):
    session = SessionFactory()
    try:
        # 요청 데이터로 Todo 객체 생성
        todo = Todo(
            title=body.title,
            is_done=body.is_done
        )
        session.add(todo)   # INSERT 준비
        session.commit()    # DB에 실제 반영 (commit이 없으면 저장 안됨)
        return todo
    finally:
        session.close()

# PATCH  /todos/{todo_id}
@app.patch(
    '/todos/{todo_id}',
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK
)
def update_todo_handler(todo_id: int, body: TodoUpdateRequest):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            # None이 아닌 값만 수정
            if body.title is not None:
                todo.title = body.title
            if body.is_done is not None:
                todo.is_done = body.is_done
            session.commit()    # DB에 반영
            return todo
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    finally:
        session.close()

# DELETE  /todos/{todo_id}
@app.delete(
    '/todos/{todo_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_todo_handler(todo_id: int):
    session = SessionFactory()
    try:
        stmt = select(Todo).where(Todo.id == todo_id)
        todo = session.execute(stmt).scalars().first()
        if todo:
            session.delete(todo)
            session.commit()
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Todo not found'
        )
    finally:
        session.close()