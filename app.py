import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="목우회 출석 통계", layout="wide")

def extract_attendance(file_path):
    """서버에 저장된 txt 파일에서 참석 인원 추출"""
    data = []
    current_date = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        for line in lines:
            # 날짜 패턴 추출 (예: --------------- 2024년 3월 14일 ... ---------------)
            date_match = re.search(r'-+ (\d{4}년 \d{1,2}월 \d{1,2}일)', line)
            if date_match:
                current_date = date_match.group(1)
                continue
            
            # 참석 명단 추출 (보통 투표 결과나 '참석 1', '참 2' 형태)
            # Han형님의 데이터 특성에 맞춰 '참석' 뒤의 숫자를 파악합니다.
            if current_date and ('참석' in line or '참 ' in line):
                num_match = re.findall(r'(\d+)', line)
                if num_match:
                    count = int(num_match[-1])
                    data.append({'날짜': current_date, '인원': count})
        
        df = pd.DataFrame(data)
        if not df.empty:
            # 날짜별로 가장 높은 참석 번호만 남김 (중복 제거)
            df = df.groupby('날짜').max().reset_index()
            # 날짜 정렬을 위해 변환
            df['날짜_dt'] = pd.to_datetime(df['날짜'], format='%Y년 %m월 %d일')
            df = df.sort_values('날짜_dt')
            return df
    except FileNotFoundError:
        st.error(f"파일을 찾을 수 없습니다: {file_path}")
        return pd.DataFrame()

# 메인 화면
st.title("🎾 목우회 출석 데이터 대시보드")
st.info("깃허브에 업로드된 대화 내용을 바탕으로 실시간 집계합니다.")

# 깃허브에 올린 파일명과 일치해야 합니다.
FILE_NAME = "KakaoTalk_20260211_1621_54_255_group.txt"
df = extract_attendance(FILE_NAME)

if not df.empty:
    # 1. 지표 표시 (최근 인원 등)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("최근 운동 날짜", df['날짜'].iloc[-1])
    with col2:
        st.metric("최근 참석 인원", f"{df['인원'].iloc[-1]}명")

    # 2. 그래프 시각화
    st.subheader("날짜별 참석자 추이")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['날짜'], df['인원'], marker='o', color='#2ecc71', linewidth=2)
    ax.fill_between(df['날짜'], df['인원'], color='#2ecc71', alpha=0.2) # 영역 색 채우기
    
    plt.xticks(rotation=45)
    ax.set_ylim(0, df['인원'].max() + 5)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # 한글 폰트 설정 (Streamlit Cloud 환경 배려)
    plt.rcParams['font.family'] = 'sans-serif' 
    
    st.pyplot(fig)

    # 3. 데이터 리스트
    with st.expander("전체 출석 데이터 보기"):
        st.table(df[['날짜', '인원']].sort_values('날짜', ascending=False))
else:
    st.warning("데이터를 불러오는 중입니다. 파일명이나 인코딩을 확인해주세요.")
