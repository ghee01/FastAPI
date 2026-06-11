from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

# http://localhost:8000/
# http://127.0.0.1:8000/

# 1. 기본 GET 엔드포인트 - 파라미터 없음
@app.get('/')
def root_handler():
    # dict 자료형 리턴 --> JSON으로 자동 변환 후 응답
    return {'message':'Hello FastAPI!'}

# 2. 추가 경로 - 파라미터 없음
@app.get('/login')
def login_handler():
    return {'message':'로그인 페이지에 오신 것을 환영합니다!'}

# 3. 경로 변수(Path Parameter)
#   - url의 일부를 변수로 받음 --> {변수명}
@app.get('/users/{user_id}')
def read_user_handler(user_id: int):
    return {'user_id':user_id, 'message':f'사용자 {user_id} 정보 조회'}

# 4. 쿼리 파라미터(Query Parameter)
#   - url 뒤 ?key=value 형태로 전달
#   - max_price: int | None == Optional[int]
@app.get('/items')
def read_items_handler(max_price: int | None=None): # 초기값 None
    return {'max_price':max_price}

# 5. Pydantic 모델 - 요청/응답 데이터 구조 정의
class Item(BaseModel):
    name: str
    price: int
    is_stock: bool=True # 기본값 True(요청 시 생략 가능)

# 6. POST - 요청 본문(Request Body) 수신
@app.post(path='/items',
          response_model=Item, # 응답 구조를 Item으로 고정
          status_code=status.HTTP_201_CREATED)
def create_item_handler(item: Item):
    return item

# 7. PUT - 경로 변수 + 쿼리 파라미터 + 요청 본문 혼합
#   - FastAPI가 파라미터 종류 자동 구분
#       - {item_id} > 경로 변수(url에 중괄호로 선언)
#       - assignee > 쿼리 파라미터(단순 타입, 경로에 없음)
#       - item: Item > 요청 본문(Pydantic 모델이면 Body)
@app.put('/items/{item_id}')
def update_item_handler(item_id: int, assignee: str, item: Item):
    return {
        'item_id':item_id,
        'assignee':assignee,
        'item':item
    }

# 8. 응답 모델(Response Model)
#   - 반환되는 데이터를 OrderResponse 형태로 필터링
#   - 서버 내부에서 민감 데이터(비밀번호 등)가 dict에 섞여 있어도
#     response_model에 정의된 필드만 클라이언트에 전달
class OrderResponse(BaseModel):
    order_id: int
    pickup: bool | None=None

# GET
@app.get('/orders/{order_id}', response_model=OrderResponse)
def get_order_handler(order_id: int, pickup: bool | None=None):
    return {
        'order_id':order_id,
        'pickup':pickup
    }