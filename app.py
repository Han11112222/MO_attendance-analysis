import streamlit as st
import streamlit.components.v1 as components
import os

# 1. 페이지를 넓게 설정
st.set_page_config(page_title="목우회 분석 리포트", layout="wide")

# 2. 형님이 업로드한 HTML 파일명 (공백과 괄호 주의)
HTML_FILE = "목우회_분석_완성본_20260212 (1).html"

def main():
    # 파일이 존재하는지 확인
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # 3. HTML 삽입 (형님이 만든 동적 그래프와 디자인이 그대로 나타남)
        # height는 대시보드 길이에 맞춰 1500으로 넉넉히 잡았습니다.
        components.html(html_content, height=1500, scrolling=True)
    else:
        st.error(f"파일을 찾을 수 없습니다: {HTML_FILE}")
        st.info("깃허브 리포지토리에 HTML 파일이 업로드되어 있는지 확인해주세요.")

if __name__ == "__main__":
    main()
