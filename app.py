import streamlit as st
import streamlit.components.v1 as components
import os

# 페이지 설정
st.set_page_config(page_title="목우회 분석 리포트", layout="wide")

# 파일 경로 설정 (2번째 사진의 깃허브 구조 기준)
html_file_path = "목우회_분석_완성본_20260212 (1).html"

def main():
    if os.path.exists(html_file_path):
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # HTML 원본의 구성을 그대로 스트림릿에 삽입
        # height는 화면 크기에 맞게 조절하세요.
        components.html(html_content, height=1500, scrolling=True)
    else:
        st.error(f"'{html_file_path}' 파일을 찾을 수 없습니다. 깃허브 파일명을 다시 확인해주세요.")

if __name__ == "__main__":
    main()
