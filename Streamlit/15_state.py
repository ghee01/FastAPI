# ===========================================================
# fastapi/Streamlit/15_state.py
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

if st.button('+1'):
    st.session_state.count += 1

st.write(f'현재 카운트: {st.session_state.count}')