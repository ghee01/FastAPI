# =====================================
# fastapi/Streamlit/03_image.py
# 
# Streamlit 라이브러리 기초 실습
# 
#   - 이미지 삽입
# =====================================

import streamlit as st
from PIL import Image

image = Image.open('bleach1.jpg')
image2 = Image.open('bleach2.jpg')

st.image(image, caption='블리치')
st.image(image2, caption='호정 13대')

st.image(image, caption='너비를 100으로 수정', width=100)
st.image(image2, caption='너비를 200으로 수정', width=200)

st.image(image, caption='전체 너비', width='stretch')
st.image(image2, caption='원본 너비', width='content')

small_image = image.resize((200,200))   # 작은 사이즈 조정
st.image(small_image, caption='작아진 이미지')