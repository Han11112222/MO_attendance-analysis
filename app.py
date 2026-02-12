import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 한글 폰트 설정 (배포 환경에 따라 나눔고딕 등을 설치하거나 기본 폰트 사용)
plt.rc('font', family='NanumGothic') 

def extract_attendance(file_content):
    """카카오톡 대화에서 날짜와 참석 인원 추출"""
    data = []
    current_date = None
    
    lines = file_content.split('\n')
    for line in lines:
        # 날짜 라인 확인 (예: --------------- 2024년 3월 14일 목요일 ---------------)
        date_match = re.search(r'-+ (\d{4}년 \d{1,2}월 \d{1,2}일) \w+요일 -+', line)
        if date_match:
            current_date = date_match.group(1)
            continue
            
        # 참석 메시지 확인 (예: [이름] [시간] 참석 1, 참 2 등)
        if current_date and ('참석' in line or '참 ' in line or '참슥' in line):
            # 숫자 추출 (참석 12 처럼 뒤에 붙은 숫자)
            num_match = re.findall(r'(\d+)', line)
            if num_match:
                count = int(num_match[-1])
                # 해당 날짜의 최대 참석 번호를 기록
                data.append({'날짜': current_date, '인원': count})

    df = pd.DataFrame(data)
    if not df.empty:
        # 날짜별 마지막(최대) 인원만 남기기
        df = df.groupby('날짜').max().reset_index()
        # 날짜 순서 정렬을 위해 datetime 변환
        df['날짜_dt'] = pd.to_datetime(df['날짜'], format='%Y년 %m월 %d일')
        df = df.sort_values('날짜_dt')
    return df

# 스트림릿 UI
st.title("🎾 목우회 참석 현황 분석")
st.write("카카오톡 대화 파일을 업로드하여 참석 인원 추이를 확인하세요.")

uploaded_file = st.file_uploader("KakaoTalk 대화 내용(.txt) 업로드", type="txt")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    df = extract_attendance(content)
    
    if not df.empty:
        st.subheader("날짜별 참석 인원 추이")
        
        # 그래프 생성
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df['날짜'], df['인원'], marker='o', linestyle='-', color='royalblue')
        ax.set_xlabel("운동 날짜")
        ax.set_ylabel("참석 인원 (명)")
        plt.xticks(rotation=45)
        ax.grid(True, linestyle='--', alpha=0.7)
        
        st.pyplot(fig)
        
        # 데이터 표 표시
        st.subheader("상세 데이터")
        st.dataframe(df[['날짜', '인원']])
    else:
        st.error("참석 데이터를 찾을 수 없습니다. 파일 형식을 확인해주세요.")
