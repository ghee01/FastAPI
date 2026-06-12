# 간단한 메모장 만들기
#   - DB없이 메모리(리스트)만 사용 --> 컴퓨터 재부팅 시 데이터 초기화
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

app = FastAPI(
    title='메모장 API',
    description='FastAPI 입문 실습용 메모장 CRUD API',
    version='1.0.0'
)

# 임시 데이터 저장소(메모리)
memos = []
next_id = 1 # 자동 증가 ID를 직접 관리(전역 변수)

# pydantic 모델 정의
#   - 메모 생성, 수정, 조회
class MemoCreate(BaseModel):
    """POST 요청 바디 - 메모 작성 시 받는 데이터"""
    content: str

class MemoUpdate(BaseModel):
    """PATCH 요청 바디 - None이 기본값 > 보내지 않으면 기존 값 유지"""
    content: Optional[str] = None

class MemoResponse(BaseModel):
    """응답으로 내보내는 메모 형태"""
    id: int
    content: str
    create_at: str # 생성 시각
    update_at: str # 수정 시각

# 헬퍼 함수
def find_memo(memo_id: int):
    """ID로 메모 검색 - 없으면 None 반환"""
    return next((m for m in memos if m['id'] == memo_id), None)

def now():
    """현재 시각을 문자열로 변환"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 엔드포인트
@app.get('/')
def home():
    """API 안내"""
    return {'message':'메모장 API입니다. /docs에서 테스트 해보세요.'}

@app.get('/memos', response_model=list[MemoResponse], status_code=status.HTTP_200_OK)
def get_memos():
    """전체 메모 목록 조회 - 메모가 없으면 빈 리스트 반환"""
    return memos

@app.get('/memos/{memo_id}', response_model=MemoResponse, status_code=status.HTTP_200_OK)
def get_memo(memo_id: int):
    """특정 메모 1개 조회 - memo_id로 조회, 없으면 404 에러 반환"""
    memo = find_memo(memo_id)
    if memo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{memo_id}번 메모를 찾을 수 없습니다.')
    return memo

@app.post('/memos', response_model=MemoResponse, status_code=status.HTTP_201_CREATED)
def create_memo(body: MemoCreate):
    """새 메모 작성 - 요청 바디: {'content':'메모 내용'}"""
    global next_id # 전역 변수임을 선언
    new_memo = {
        'id':next_id,
        'content':body.content,
        'create_at':now(),
        'update_at':now()
        }
    next_id += 1
    memos.append(new_memo)
    return new_memo

@app.patch('/memos/{memo_id}', response_model=MemoResponse, status_code=status.HTTP_200_OK)
def update_memo(memo_id: int, body: MemoUpdate):
    """
    메모 수정(부분 수정) - content만 보내면 content만 수정,
                          update_at은 자동 갱신
    """
    memo = find_memo(memo_id)
    if memo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{memo_id}번 메모를 찾을 수 없습니다.')
    if body.content is not None:
        memo['content'] = body.content
    memo['update_at'] = now()
    return memo

@app.delete('/memos/{memo_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_memo(memo_id: int):
    """메모 삭제 - 성공 204, 실패 404"""
    memo = find_memo(memo_id)
    if memo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{memo_id}번 메모를 찾을 수 없습니다.')
    memos.remove(memo)