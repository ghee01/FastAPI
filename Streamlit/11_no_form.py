# ===========================================================
# fastapi/Streamlit/11_no_form.py
# 
#   - 왜 폼이 필요할까?
#       문제 상황 살펴보기(폼이 없는 경우)
#           이름을 한 글자씩 입력할 때마다 화면 전체 재실행
#           위젯이 3~4개밖에 없다면 문제되지 않지만,
#           위젯이 많아지거나 뒤쪽에 무거운 연산이 있으면
#           매 글자 입력할 때마다 연산이 반복 실행되어 비효율적
#           해결 위젯 → st.form
# ===========================================================

import streamlit as st

st.title('회원가입 (문제 상황)')

name = st.text_input('이름')
email = st.text_input('이메일')
age = st.number_input('나이', min_value=0, max_value=120)

st.divider()

st.write(f'입력한 이름 : {name}')