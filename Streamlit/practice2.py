import streamlit as st
import pandas as pd

st.title('CSV 데이터 필터링 앱')

file = st.file_uploader(
    'CSV 파일을 업로드하세요',
    type='csv',
    accept_multiple_files=False
)

if file is not None:
    st.write('업로드 된 데이터 미리보기')
    df = pd.read_csv(file)
    st.dataframe(df)
    
    st.divider()

    select_col = st.multiselect('확인하고 싶은 열을 선택하세요', df.columns)
    numeric_col = df.select_dtypes(include='number').columns.tolist()
    if numeric_col:
        filter_col = st.selectbox('범위로 필터링할 열을 선택하세요', numeric_col)

        min_val = int(df[filter_col].min())
        max_val = int(df[filter_col].max())

        start_val, end_val = st.slider(
            f'{filter_col} 범위 선택',
            min_value=min_val,
            max_value=max_val,
            value=(min_val, max_val)
        )

        st.divider()

        result = df[(df[filter_col] >= start_val) & (df[filter_col] <= end_val)]
        result = result[select_col]
        st.text(f'필터링 결과 ({len(result)}건)')
        st.write(result)
else:
    st.info('CSV 파일을 업로드해주세요.')