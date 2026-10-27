import random
import time
import urllib.parse
import streamlit as st

# 1. 페이지 기본 설정 (웹 브라우저 탭 제목, 아이콘, 레이아웃)
st.set_page_config(
    page_title="인생의 결정 장애 해결사 & 위치 기반 AI 룰렛",
    page_icon="🎯",
    layout="centered"
)

# 2. 메인 화면 타이틀 및 설명
st.title("🎯 인생의 결정 장애 해결사!")
st.caption("선택하기 힘들 땐 위치와 함께 AI 룰렛에게 맡겨보세요!")

# 3. 사이드바 - 테마 선택 기능
st.sidebar.header("⚙️ 룰렛 설정")
option = st.sidebar.selectbox(
    "어떤 결정을 내릴까요?",
    ["🍱 오늘 점심 메뉴", "🎮 주말에 할 일", "✏️ 직접 입력하기"]
)

# 4. 선택한 테마에 따른 기본 후보 데이터 설정
if option == "🍱 오늘 점심 메뉴":
    default_candidates = "제육볶음, 돈까스, 마라탕, 김치찌개, 초밥, 햄버거"
elif option == "🎮 주말에 할 일":
    default_candidates = "밀린 OTT 보기, 카페 가서 공부, 침대와 일체화, 친구 만나기, 운동하기"
else:
    default_candidates = ""

# 5. 사용자 입력 받기 (위치 및 후보 목록)
st.subheader("1. 현재 위치 입력")
location = st.text_input(
    "📍 지금 계신 위치(동/구 또는 장소명)를 입력하세요:",
    placeholder="예: 용인시 수지구, 강남역, 홍대입구 등"
)

st.subheader("2. 후보 목록 설정")
user_input = st.text_area(
    "후보 목록을 입력하세요 (쉼표로 구분):",
    value=default_candidates,
    height=120
)

# 6. 추첨 실행 버튼 및 예외 처리
if st.button("🎲 운명의 선택 실행!", use_container_width=True):
    # 예외 처리 1: 위치를 입력하지 않은 경우 안내 메시지 출력
    if not location.strip():
        st.warning("⚠️ 먼저 현재 위치를 입력해 주세요!")
    else:
        # 예외 처리 2: 입력받은 후보 목록 검증 및 양쪽 공백 제거
        candidates = [item.strip() for item in user_input.split(",") if item.strip()]
        
        if not candidates:
            st.warning("⚠️ 선택할 후보를 하나 이상 입력해 주세요!")
        else:
            # 긴장감을 주는 로딩 효과 연출
            with st.spinner("AI가 위치 정보와 함께 운명을 분석 중입니다..."):
                time.sleep(1.5)
            
            # 무작위 추첨 실행
            selected = random.choice(candidates)
            
            # 카카오맵 검색용 URL 인코딩 생성 (위치 + 당첨된 메뉴/활동)
            search_query = f"{location} {selected}"
            encoded_query = urllib.parse.quote(search_query)
            map_url = f"https://map.kakao.com/link/search/{encoded_query}"
            
            # 결과 및 풍선 애니메이션 효과 출력
            st.balloons()
            st.success("🎉 결정 완료!")
            st.markdown(f"### 📍 현재 위치: **{location}**")
            st.markdown(f"### 👑 오늘 당신의 선택은: **[{selected}]** 입니다!")
            
            # 지도 검색 버튼 연결
            st.markdown(f"👉 [🔍 '{location} {selected}' 카카오맵으로 바로 장소 검색하기]({map_url})")
            st.info("💡 팁: 결과가 맘에 안 든다면... 한 번 더 누르는 것도 당신의 운명입니다!")
