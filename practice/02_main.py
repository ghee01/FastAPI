from fastapi import FastAPI

app = FastAPI()

# 서버 실행
@app.get('/')
def root_handler():
    return {'message':'Hello, FastAPI!'}

# 경로 사용
@app.get('/login') # GET요청과 경로 매핑 설정
def login_handler(): # 요청 처리하는 함수 정의
    return {'message':'로그인 페이지에 오신 것을 환영합니다'}

# 동적 경로 사용 --> /users/1, /users/2, ..
# 사용자 아이디마다 별도의 경로 정의 필요 없이 하나의 경로 /users/{user_id} 정의
# 동일한 패턴의 여러 요청에 대응 가능

# 경로 변수 사용
@app.get('/users/{user_id}')
def read_user_handler(user_id: int):
    return {'user_id':user_id, 'message':f'사용자 {user_id} 정보 조회'}

# 쿼리 파라미터 사용
@app.get('/items')
def read_items_handler(max_price: int | None=None):
    # int 또는 None, 기본값은 None
    return {'max_price':max_price}
# 경로 변수와 쿼리 파라미터는 둘 다 엔드포인트 함수의 매개변수로 사용됨
# 경로 변수: 경로에서 값 추출
# 쿼리 파라미터: 경로 뒤에 ?key=value 형태로 덧붙은 값 추출