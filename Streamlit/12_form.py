# ===========================================================
# fastapi/Streamlit/12_form.py
# 
#   - 폼 위젯
#       - 여러 입력 한 번에 제출 가능
#       - 폼 제출 시 입력값을 검증하고 처리 편하다
#       - 블록 안의 위젯들은 값이 바뀌어도 즉시 재실행 되지 않고,
#         제출 버튼을 누르는 순간에만 한꺼번에 재실행 된다
#         → 성능, 사용성 개선
# ===========================================================

import streamlit as st

st.title('회원가입 (폼 적용)')

# 'signup_form': 폼을 구분하는 고유한 이름(key), 폼이 여러 개면 서로 다른 이름을 주어야 한다
with st.form('signup_form'):
    name = st.text_input('이름')
    email = st.text_input('이메일')
    age = st.number_input('나이', min_value=0, max_value=120)

    # 일반 버튼 위젯이 아니고 폼 안에서만 쓸 수 있는 버튼 위젯을 사용해야 한다
    submitted = st.form_submit_button('가입하기')

# 버튼을 클릭 → 폼 제출 시점의 최종값을 그대로 가지고 있다
if submitted:
    st.success(f'{name}님, 가입 완료! (이메일: {email}, 나이: {age})')