import streamlit as st
import streamlit.components.v1 as components
import json
import re

# 페이지 설정
st.set_page_config(page_title="목우회 분석 리포트", layout="wide")

def load_and_process_data(file_path):
    """txt 파일을 읽어 HTML이 이해할 수 있는 JSON 구조로 변환"""
    processed_data = []
    current_date = None
    
    # 성함 정제 함수 (HTML의 cleanName 로직 반영)
    def clean_name(raw):
        name = re.sub(r'목우회|테니스|님|씨|총무|회장|이사|코치|프로', '', raw)
        name = re.sub(r'\(.*?\)|\[.*?\]|\d+', '', name).strip()
        return name if name else raw

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            # 날짜 인식
            date_match = re.search(r'(\d{4})[년.\-\s]+(\d{1,2})[월.\-\s]+(\d{1,2})[일.\-\s]?', line)
            if date_match:
                current_date = f"{date_match.group(1)}-{date_match.group(2).zfill(2)}-{date_match.group(3).zfill(2)}"
                continue
            
            # 참석 데이터 인식 (메시지 패턴)
            msg_match = re.match(r'^\[(.*?)\]\s*\[(.*?)\]\s*(.*)', line)
            if msg_match and current_date:
                raw_name = msg_match.group(1)
                content = msg_match.group(3)
                
                # 참석 숫자 추출
                cham_match = re.search(r'(?:참|참석|참여|참가)[^\d]*(\d+)', content)
                if cham_match:
                    count = int(cham_match.group(1))
                    if 0 < count < 60:
                        processed_data.append({
                            "date": current_date,
                            "name": clean_name(raw_name),
                            "count": count,
                            "rawName": raw_name
                        })
        return processed_data
    except Exception as e:
        st.error(f"파일 로드 오류: {e}")
        return []

# 1. 데이터 로드 (깃허브에 올린 파일명)
FILE_NAME = "KakaoTalk_20260211_1621_54_255_group.txt"
data_json = load_and_process_data(FILE_NAME)

# 2. Han형님의 HTML 템플릿 로드 및 데이터 주입
# (HTML 파일도 같은 경로에 있어야 합니다)
try:
    with open("목우회_분석_완성본_20260212 (1).html", "r", encoding="utf-8") as f:
        html_template = f.read()

    # HTML 내의 window.preloadedData 부분을 실제 데이터로 교체
    # 기존에 샘플 데이터가 들어있던 부분을 찾아 갈아끼웁니다.
    data_injection = f"window.preloadedData = {json.dumps(data_json, ensure_ascii=False)};"
    
    # 정규표현식으로 preloadedData 할당 부분 교체
    final_html = re.sub(r'window\.preloadedData\s*=\s*\[.*?\];', data_injection, html_template)

    # 3. 스트림릿에 HTML 표시 (동적 그래프 작동)
    components.html(final_html, height=1200, scrolling=True)

except FileNotFoundError:
    st.error("HTML 템플릿 파일을 찾을 수 없습니다. 깃허브에 함께 업로드했는지 확인해주세요!")
