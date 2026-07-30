# ===========================================================
# fastapi/Streamlit/16_state_callback.py
# 
# session_state
#   - 위젯을 조작할 때마다 일반 파이썬 변수가 초기화 되는 문제 해결
#   - st.session_state로 재실행 사이의 값 유지 가능
#   - 콜백 함수와 함께 사용 가능
# ===========================================================

import streamlit as st

st.title('카운터 (session state 적용)')

# session_state : 브라우저 탭(세션) 하나에 묶여서 재실행 돼도 값이 사라지지 않는 딕셔너리 형태의 특수 저장소
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment():
    """콜백 함수 : 위젯 클릭 시 화면이 다시 그려지기 직전에 자동으로 호출되는 함수"""
    st.session_state.count += 1

def decrement():
    st.session_state.count -= 1

def reset():
    # 콜백 안에서는 조건문 없이 바로 대입
    st.session_state.count = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.button('+ 증가', on_click=increment) # 함수 이름만 전달 (클릭 시에만 실행)

with col2:
    st.button('- 감소', on_click=decrement)

with col3:
    st.button('리셋', on_click=reset)

# st.metric : 카드 형태
st.metric('현재 카운트', st.session_state.count)