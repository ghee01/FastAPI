# =====================================
# fastapi/Streamlit/02_button.py
# 
# Streamlit 라이브러리 기초 실습
# 
#   - code 삽입
#   - 버튼 삽입
# =====================================

import streamlit as st

code = 'print("Hello, world!")'
code2 = 'printf("Hello, world!")'
code3 = '<a href="https://www.naver.com">네이버</a>'

st.code(code, language='python')
st.code(code2, language='C')
st.code(code3, language='html')

st.write('---')

st.button('클릭하시오', type='primary')

if st.button('Reset', type='primary', key='btn1'):
    st.write('Reset 버튼을 눌렀습니다')

if st.button('Cancel', type='secondary', key='btn2'):
    st.write('cancel 버튼을 눌렀습니다')

if st.button('Ignore', type='tertiary', key='btn3'):
    st.write('Ignore 버튼을 눌렀습니다')

def button_write():
    st.title('Title')

st.button('activate', on_click=button_write)    # 클릭하면 함수 실행