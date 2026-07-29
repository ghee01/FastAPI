# ========================================================
# fastapi/Streamlit/08_layout.py
# 
# Streamlit 라이브러리 기초 실습
# 
#   - 레이아웃
# ========================================================

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 메인 페이지
st.title('This is main page')

# sidebar
with st.sidebar:
    st.title('This is sidebar')
    side_option = st.multiselect(
        label='your selection is',
        options=['Car', 'Airplane', 'Train', 'Ship', 'Bicycle'],
        placeholder='select transportation'
    )

# 이미지 하나씩
img1 = Image.open('bleach1.jpg')
img2 = Image.open('bleach2.jpg')

st.header('Bleach')
st.image(img1, width=400, caption='Bleach illust')

st.header('Shinigami')
st.image(img2, width=400, caption='Shinigami illust')

# 컬럼 레이아웃 (세로 단 2개)
col1, col2 = st.columns(2)  # 똑같은 비율

with col1:
    st.header('Bleach')
    st.image(img1, width=300, caption='Bleach illust')

with col2:
    st.header('Shinigami')
    st.image(img2, width=300, caption='Shinigami illust')

st.divider()

# 탭 레이아웃
tab1, tab2 = st.tabs(['실습1', '실습2'])

# 판다스로 csv 불러와서 데이터프레임 생성
df = pd.read_csv('../storage_cafe/input/orders.csv')

with tab1:  # 실습1
    st.table(df.head())

with tab2:  # 실습2
    fig, ax = plt.subplots()
    sns.countplot(data=df, ax=ax)
    st.pyplot(fig)