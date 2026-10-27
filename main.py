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

# 4. 먹거리 / 할거리 아이디어 및 이미지 추천 파트
st.subheader("2. 추천 아이디어 & 이미지 둘러보기")

# 안정적인 이미지 URL 데이터 셋
FOOD_RECOMMENDATIONS = [
    {"name": "돈까스", "img": "https://cdn.pixabay.com/photo/2021/01/16/09/05/pork-cutlet-5921509_640.jpg", "desc": "바삭하고 고소한 일식/경양식 돈까스"},
    {"name": "마라탕", "img": "https://cdn.pixabay.com/photo/2017/08/06/06/43/soup-2589574_640.jpg", "desc": "얼큰하고 알싸한 중식 마라탕"},
    {"name": "초밥", "img": "https://cdn.pixabay.com/photo/2017/10/15/11/41/sushi-2853382_640.jpg", "desc": "신선하고 깔끔한 모듬 초밥"},
    {"name": "햄버거", "img": "https://cdn.pixabay.com/photo/2016/03/05/19/02/hamburger-1238246_640.jpg", "desc": "육즙 가득한 수제 버거"},
    {"name": "제육볶음", "img": "https://cdn.pixabay.com/photo/2017/04/04/16/55/korean-food-2202111_640.jpg", "desc": "매콤달콤 든든한 한식 제육 덮밥/정식"},
    {"name": "파스타", "img": "https://cdn.pixabay.com/photo/2018/07/18/19/12/pasta-3547078_640.jpg", "desc": "꾸덕한 크림 & 상큼한 토마토 파스타"}
]

ACTIVITY_RECOMMENDATIONS = [
    {"name": "카페 가서 공부", "img": "https://cdn.pixabay.com/photo/2015/05/31/10/54/coffee-791045_640.jpg", "desc": "조용한 스터디카페에서 자기계발"},
    {"name": "친구 만나기", "img": "https://cdn.pixabay.com/photo/2017/07/31/11/21/people-2557396_640.jpg", "desc": "보드게임카페에서 신나는 게임 한 판"},
    {"name": "밀린 OTT 보기", "img": "https://cdn.pixabay.com/photo/2016/11/18/14/05/brick-wall-1834784_640.jpg", "desc": "영화관 특별관이나 넷플릭스 정주행"},
    {"name": "침대와 일체화", "img": "https://cdn.pixabay.com/photo/2016/11/29/03/53/quiet-1867185_640.jpg", "desc": "아늑한 만화카페에서 누워서 만화책 보기"},
    {"name": "운동하기", "img": "https://cdn.pixabay.com/photo/2017/08/07/14/02/man-2604149_640.jpg", "desc": "헬스장이나 피트니스 센터에서 땀 흘리기"},
    {"name": "산책하기", "img": "https://cdn.pixabay.com/photo/2014/07/05/08/38/park-384659_640.jpg", "desc": "근처 공원 시원한 바람 맞으며 걷기"}
]

if option == "🍱 오늘 점심/저녁 먹거리":
    st.info("💡 어떤 음식들이 당기는지 이미지로 확인하고 추천받아 보세요!")
    rec_col1, rec_col2 = st.columns([3, 1])
    with rec_col2:
        if st.button("🔄 다른 먹거리 추천 보기"):
            st.rerun()
            
    # 무작위로 3개 음식 추천 추출
    sampled_foods = random.sample(FOOD_RECOMMENDATIONS, k=min(3, len(FOOD_RECOMMENDATIONS)))
    cols = st.columns(3)
    for idx, item in enumerate(sampled_foods):
        with cols[idx]:
            try:
                st.image(item["img"], use_container_width=True)
            except Exception:
                st.write("🖼️ (이미지 로딩 불가)")
            st.markdown(f"**{item['name']}**")
            st.caption(item["desc"])

    # 추천 항목들을 후보 목록에 추가하는 버튼
    if st.button("➕ 위 추천 먹거리 3개를 후보 목록에 담기"):
        food_names = [f["name"] for f in sampled_foods]
        st.session_state.candidates_text = ", ".join(food_names)
        st.success("후보 목록에 담겼습니다!")

elif option == "🎮 주말에 즐길 할거리":
    st.info("💡 주말에 무얼 하며 놀지 매장 및 활동 분위기를 확인해 보세요!")
    rec_col1, rec_col2 = st.columns([3, 1])
    with rec_col2:
        if st.button("🔄 다른 할거리 추천 보기"):
            st.rerun()
            
    # 무작위로 3개 활동 추천 추출
    sampled_acts = random.sample(ACTIVITY_RECOMMENDATIONS, k=min(3, len(ACTIVITY_RECOMMENDATIONS)))
    cols = st.columns(3)
    for idx, item in enumerate(sampled_acts):
        with cols[idx]:
            try:
                st.image(item["img"], use_container_width=True)
            except Exception:
                st.write("🖼️ (이미지 로딩 불가)")
            st.markdown(f"**{item['name']}**")
            st.caption(item["desc"])

    if st.button("➕ 위 추천 할거리 3개를 후보 목록에 담기"):
        act_names = [a["name"] for a in sampled_acts]
        st.session_state.candidates_text = ", ".join(act_names)
        st.success("후보 목록에 담겼습니다!")

else:
    st.write("원하시는 후보를 아래 3번 항목에 직접 작성해 주세요.")

st.divider()

# 5. 후보 목록 설정
st.subheader("3. 룰렛 후보 목록 설정")
user_input = st.text_area(
    "후보 목록을 쉼표(,)로 구분하여 직접 작성하거나 위에서 담아보세요:",
    value=st.session_state.candidates_text,
    placeholder="예: 제육볶음, 돈까스, 초밥 (또는 직접 원하는 항목 작성)",
    height=100
)

# 6. 추첨 및 카카오맵 매핑 실행
if st.button("🎲 운명의 선택 실행!", use_container_width=True):
    if not location.strip():
        st.warning("⚠️ 먼저 현재 위치를 입력해 주세요!")
    else:
        candidates = [item.strip() for item in user_input.split(",") if item.strip()]
        
        if not candidates:
            st.warning("⚠️ 룰렛을 돌릴 후보를 하나 이상 입력해 주세요!")
        else:
            with st.spinner("AI가 위치 정보와 함께 운명을 심도 있게 분석 중입니다..."):
                time.sleep(1.5)
            
            selected = random.choice(candidates)
            
            # 장소 검색 키워드 자동 매핑 딕셔너리
            keyword_map = {
                "밀린 OTT 보기": "영화관",
                "카페 가서 공부": "스터디카페",
                "침대와 일체화": "만화카페",
                "친구 만나기": "보드게임카페",
                "운동하기": "헬스장",
                "산책하기": "공원"
            }
            
            search_keyword = keyword_map.get(selected, selected)
            search_query = f"{location} {search_keyword}"
            encoded_query = urllib.parse.quote(search_query)
            map_url = f"https://map.kakao.com/link/search/{encoded_query}"
            
            st.balloons()
            st.success("🎉 결정 완료!")
            st.markdown(f"### 📍 현재 위치: **{location}**")
            st.markdown(f"### 👑 오늘 당신의 선택은: **[{selected}]** 입니다!")
            
            st.markdown(f"👉 [🔍 '{location} {search_keyword}' 카카오맵에서 추천 장소 검색하기]({map_url})")
            st.info("💡 팁: 결과가 맘에 안 든다면... 한 번 더 누르는 것도 당신의 운명입니다!")
