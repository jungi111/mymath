import streamlit as st
import asyncio
from main import MathProblemGenerator

# MathProblemGenerator 객체를 세션 상태에 저장
if 'generator' not in st.session_state:
    st.session_state['generator'] = MathProblemGenerator()

# 학년과 주제 데이터 설정
subjects = {
    "중1-1": ["소인수분해", "문자와 식", "방정식", "기본 도형", "통계"],
    "중1-2": ["확률", "집합과 함수", "일차 함수", "기하", "수와 연산"],
    "중2-1": ["다항식", "방정식", "부등식", "도형의 성질", "확률과 통계"],
    "중2-2": ["함수", "기하", "이차 함수", "삼각형", "원"],
    "중3-1": ["집합", "명제", "함수", "수열", "순열과 조합"],
    "중3-2": ["미분", "적분", "벡터", "확률", "통계"]
}

# Streamlit 앱 구성
st.title("Math Problem Generator")

# 첫 번째 콤보박스: 학년 선택
grade = st.selectbox("Select Grade", list(subjects.keys()))

# 두 번째 콤보박스: 주제 선택
topic = st.selectbox("Select Topic", subjects[grade])

# 문제 생성 버튼
if st.button("Generate Question"):
    generator = st.session_state['generator']
    # 비동기 함수 호출
    response = asyncio.run(generator.generate_question(topic))
    st.session_state['response'] = response

# 문제 출력
if 'response' in st.session_state:
    question = st.session_state['response'].get('question', '')
    st.text_area("Generated Question", question, height=100)
    
    # 정답 및 해설 보기 버튼
    if st.button("Show Answer and Description"):
        answer = st.session_state['response'].get('answer', '')
        description = st.session_state['response'].get('description', '')
        st.text_area("Answer", answer, height=100)
        st.text_area("Description", description, height=150)
