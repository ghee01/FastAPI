# ==========================================================================================
# routers/todo.py
#   - '할 일(Todo)'과 관련된 API 엔드포인트들을 모아놓은 라우터 파일
#   - main.py에서 app.include_router(todo_router)로 등록되어야 실제로 동작
# 
# 라우터(router)
#   - 웹 애플리케이션에서 여러 API를 기능별로 구분해 한 곳에 모아두기 위한 단위
#   - 서로 관련된 API 엔드포인트들을 하나의 모듈로 묶을 수 있어
#     코드를 기능 단위로 정리하고 관리하기 좋다
# 
# 라우팅(routing)
#   - 클라이언트로부터 들어온 요청(HTTP 메서드 + URL 경로)을 어떤 함수가 처리할지 연결하는 과정
#   - 연결 과정을 관리하는 역할
#   - FastAPI에서는 APIRouter 클래스를 사용해 연관된 경로들을
#     하나의 라우터로 묶고, 등록하고, 기능별로 나눈다
# ==========================================================================================

from fastapi import HTTPException, APIRouter
from sqlalchemy import select
from starlette import status
from database.db_connection import SessionFactory
from models import Todo
from schema.response import TodoResponse
from schema.request import TodoCreateRequest, TodoUpdateRequest

# APIRouter : 여러 개의 엔드포인트를 하나로 묶어서 관리하는 "작은 FastAPI 앱"
router = APIRouter(tags=['Todo'])   # Todo라는 그룹으로 묶여서 보인다

@router.get(
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

@router.get(
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

@router.post(
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

@router.patch(
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

@router.delete(
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