import random
import time
import urllib.parse
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="인생의 결정 장애 해결사 & AI 룰렛",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 인생의 결정 장애 해결사!")
st.caption("선택하기 힘들 땐 이미지 추천을 받고 위치와 함께 AI 룰렛을 돌려보세요!")

# 2. 사이드바 - 테마 선택
st.sidebar.header("⚙️ 룰렛 설정")
option = st.sidebar.selectbox(
    "어떤 결정을 내릴까요?",
    ["🍱 오늘 점심/저녁 먹거리", "🎮 주말에 즐길 할거리", "✏️ 직접 입력하기"]
)

# 세션 상태 초기화 (후보 목록 및 추천 새로고침 관리)
if "candidates_text" not in st.session_state:
    st.session_state.candidates_text = ""

# 3. 위치 입력
st.subheader("1. 현재 위치 입력")
location = st.text_input(
    "📍 지금 계신 위치(동/구 또는 장소명)를 입력하세요:",
    placeholder="예: 용인시 수지구, 강남역, 홍대입구 등"
)

# 4. 먹거리 / 할거리 아이디어 및 이미지 추천 파트 (후보 목록 전에 위치)
st.subheader("2. 추천 아이디어 & 이미지 둘러보기")
