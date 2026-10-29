import random
import re
import time
import urllib.parse
import streamlit as st

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="결정장애 해결사 | AI 룰렛 & 오늘 메뉴 및 주말 놀거리 추천",
    page_icon="🎯",
    layout="centered"
)

# 💡 구글 검색 로봇(SEO) 최적화 메타 태그 (화면에 글자가 출력되지 않도록 수정 완료)
seo_html = """
    <meta name="description" content="인생의 결정장애 해결사! 오늘 점심 메뉴, 저녁 메뉴, 주말 할거리 및 데이트 코스가 고민될 때 AI 룰렛으로 한 번에 결정하고 카카오맵 위치 검색까지 해보세요.">
    <meta name="keywords" content="결정장애 해결사, 결정장애, AI 룰렛, 메뉴 추천, 오늘 뭐먹지, 주말에 뭐하지, 점심 추천, 룰렛 추천">
    <meta name="author" content="결정장애 해결사">
    <meta property="og:type" content="website">
    <meta property="og:title" content="결정장애 해결사 - AI 룰렛 & 위치 기반 추천">
    <meta property="og:description" content="결정하기 힘들 땐 AI 룰렛에게 맡겨보세요! 먹거리/놀거리 100종 데이터 및 카카오맵 위치 검색 연동">
"""
st.markdown(seo_html, unsafe_allow_html=True)

# 2. 메인 타이틀 및 안내 문구
st.title("🎯 인생의 결정장애 해결사!")
st.caption("선택하기 힘들 땐 먹거리/할거리를 추천받고 위치와 함께 AI 룰렛을 돌려보세요!")
# 2. 사이드바 - 테마 선택
st.sidebar.header("⚙️ 룰렛 설정")
option = st.sidebar.selectbox(
    "어떤 결정을 내릴까요?",
    ["🍱 오늘 먹거리 (100종 데이터)", "🎮 주말 할거리 (100종 데이터)", "✏️ 직접 입력하기"]
)

# 세션 상태 초기화
if "candidates_text" not in st.session_state:
    st.session_state.candidates_text = ""
if "food_sample" not in st.session_state:
    st.session_state.food_sample = []
if "act_sample" not in st.session_state:
    st.session_state.act_sample = []

# 3. 위치 입력
st.subheader("1. 현재 위치 입력")
location = st.text_input(
    "📍 지금 계신 위치(동/구 또는 장소명)를 입력하세요:",
    placeholder="예: 용인시 수지구, 강남역, 홍대입구 등"
)

# ---------------------------------------------------------
# 🍽️ 100가지 대표 음식 데이터베이스
# ---------------------------------------------------------
FOOD_100 = [
    # 한식 (30가지)
    "제육볶음", "김치찌개", "된장찌개", "부대찌개", "순두부찌개", "청국장", "갈비탕", "설렁탕", 
    "순대국", "뼈해장국", "삼계탕", "닭볶음탕", "찜닭", "불고기", "삼겹살", "돼지갈비", 
    "족발", "보쌈", "비빔밥", "돌솥비빔밥", "육회비빔밥", "떡만둣국", "칼국수", "수제비", 
    "잔치국수", "비빔국수", "콩국수", "아구찜", "해물찜", "낙지볶음",
    
    # 일식/분식 (20가지)
    "돈까스", "치즈돈까스", "모듬초밥", "연어덮밥(사케동)", "가츠동", "텐동", "우동", "라멘", 
    "소바", "야키소바", "오코노미야키", "떡볶이", "로제떡볶이", "순대", "모듬튀김", "김밥", 
    "참치김밥", "쫄면", "라면", "오뎅탕",
    
    # 중식 (15가지)
    "짜장면", "간짜장", "짬뽕", "차돌짬뽕", "탕수육", "꿔바로우", "마라탕", "마라샹궈", 
    "양꼬치", "볶음밥", "잡채밥", "유린기", "깐풍기", "칠리새우", "딤섬",
    
    # 양식/패스트푸드 (20가지)
    "수제버거", "싸이버거", "치즈피자", "페퍼로니피자", "고르곤졸라피자", "까르보나라", "알리오올리오", 
    "토마토파스타", "로제파스타", "봉골레파스타", "바베큐폭립", "티본스테이크", "리조또", "도리아", 
    "샌드위치", "파니니", "샐러드", "치킨", "양념치킨", "뿌링클치킨",
    
    # 아시안/기타 (15가지)
    "쌀국수", "분짜", "팟타이", "나시고랭", "푸팟퐁커리", "인도카레", "케밥", "타코", 
    "퀘사디아", "부리또", "샤브샤브", "훠궈", "월남쌈", "스키야키", "곱창전골"
]

# ---------------------------------------------------------
# 🎮 100가지 주말 할거리/놀거리 데이터베이스
# ---------------------------------------------------------
ACTIVITY_100 = [
    # 엔터테인먼트/카페
    {"name": "카페 가서 공부", "icon": "☕", "desc": "조용한 스터디카페에서 자기계발"},
    {"name": "친구 만나기", "icon": "🎲", "desc": "보드게임카페에서 신나는 게임 한 판"},
    {"name": "밀린 OTT 보기", "icon": "🎬", "desc": "영화관 특별관이나 넷플릭스 정주행"},
    {"name": "침대와 일체화", "icon": "📚", "desc": "아늑한 만화카페에서 누워서 만화책 보기"},
    {"name": "코인노래방 가기", "icon": "🎤", "desc": "신나게 목청껏 노래 부르고 스트레스 해소"},
    {"name": "방탈출 카페 가기", "icon": "🔐", "desc": "스릴 넘치는 추리와 단서 찾기 몰입"},
    {"name": "오락실 가서 게임하기", "icon": "🕹️", "desc": "추억의 오락실과 신나는 펌프/레이싱"},
    {"name": "VR 체험하기", "icon": "🥽", "desc": "가상현실 속 롤러코스터와 액션 즐기기"},
    {"name": "대형 카페 투어", "icon": "🍰", "desc": "전경 좋은 루프탑/베이커리 카페 방문"},
    {"name": "독립서점 구경하기", "icon": "📖", "desc": "감성 넘치는 동네 책방과 굿즈 둘러보기"},
    {"name": "룸카페 가기", "icon": "🛋️", "desc": "편안하게 보드게임과 영상 감상하기"},
    {"name": "라이브 펍 가기", "icon": "🎷", "desc": "재즈/인디밴드 음악 들으며 맥주 한 잔"},
    {"name": "와인바 탐방", "icon": "🍷", "desc": "분위기 좋은 곳에서 나만의 와인 취향 찾기"},
    {"name": "LP 바 가기", "icon": "📻", "desc": "아날로그 감성 LP 음악 청음하기"},
    {"name": "포토부스 사진 찍기", "icon": "📸", "desc": "인생네컷 포토부스에서 추억 남기기"},
    {"name": "고양이 카페 가기", "icon": "🐱", "desc": "귀여운 고양이들과 힐링 타임"},
    {"name": "강아지 카페 가기", "icon": "🐶", "desc": "댕댕이들과 교감하며 스트레스 풀기"},
    {"name": "라쿤/이색 카페 가기", "icon": "🦝", "desc": "희귀 동물 카페 체험하기"},
    {"name": "칵테일바 가기", "icon": "🍸", "desc": "직접 제조하는 예쁜 칵테일 즐기기"},
    {"name": "식물원 카페 가기", "icon": "🌿", "desc": "초록빛 온실 카페에서 힐링하기"},

    # 스포츠/액티비티
    {"name": "운동하기", "icon": "🏋️‍♂️", "desc": "헬스장이나 피트니스 센터에서 땀 흘리기"},
    {"name": "실내 클라이밍", "icon": "🧗‍♀️", "desc": "볼더링 코스 정복하고 성취감 느끼기"},
    {"name": "볼링 치기", "icon": "🎳", "desc": "신나는 음악과 스트라이크 도전"},
    {"name": "당구/포켓볼 치기", "icon": "🎱", "desc": "친구들과 내기 포켓볼 한 판"},
    {"name": "실내 골프/스크린골프", "icon": "⛳", "desc": "쾌적한 스크린 골프장에서 샷 연마"},
    {"name": "테니스/실내테니스", "icon": "🎾", "desc": "라켓 스포츠로 박진감 넘치게 운동"},
    {"name": "배드민턴 치기", "icon": "🏸", "desc": "체육관이나 약수터에서 가볍게 즐기기"},
    {"name": "탁구 치기", "icon": "🏓", "desc": "스피디하고 유쾌한 핑퐁 맞대결"},
    {"name": "실내 사격 체험", "icon": "🎯", "desc": "권총/소총 실내 사격장에서 집중력 발휘"},
    {"name": "실내 양궁 체험", "icon": "🏹", "desc": "과녁 중앙 10점을 향해 활 쏘기"},
    {"name": "수영하기", "icon": "🏊‍♂️", "desc": "실내 수영장에서 전신 운동하기"},
    {"name": "요가/필라테스", "icon": "🧘‍♀️", "desc": "몸과 마음의 밸런스 잡기"},
    {"name": "자전거 라이딩", "icon": "🚴‍♂️", "desc": "한강/천변 따라 시원하게 달리기"},
    {"name": "스케이트 타기", "icon": "⛸️", "desc": "아이스링크장에서 스케이팅 즐기기"},
    {"name": "실내 서핑 체험", "icon": "🏄‍♂️", "desc": "인공 파도 위에서 서핑 즐기기"},
    {"name": "스쿼시 치기", "icon": "🎾", "desc": "벽 치기 운동으로 칼로리 대폭 소모"},
    {"name": "인라인 스케이트", "icon": "🛼", "desc": "롤러스케이트장에서 레트로 감성 내기"},
    {"name": "풋살하기", "icon": "⚽", "desc": "친구들과 풋살장에서 미니 축구"},
    {"name": "농구하기", "icon": "🏀", "desc": "길거리 농구코트에서 슛 연습"},
    {"name": "플라잉 요가", "icon": "🧘‍♂️", "desc": "해먹에 몸을 맡기고 유연성 기르기"},

    # 야외/나들이
    {"name": "산책하기", "icon": "🌳", "desc": "근처 공원 시원한 바람 맞으며 걷기"},
    {"name": "등산하기", "icon": "⛰️", "desc": "가까운 산 정상에 올라 풍경 감상"},
    {"name": "캠핑/글램핑", "icon": "⛺", "desc": "불멍과 맛있는 바베큐 파티"},
    {"name": "피크닉/돗자리 나들이", "icon": "🧺", "desc": "공원에서 도시락 먹으며 눕기"},
    {"name": "놀이공원 가기", "icon": "🎢", "desc": "에버랜드/롯데월드 롤러코스터 즐기기"},
    {"name": "아쿠아리움 방문", "icon": "🐠", "desc": "신비로운 바다 생물 구경하기"},
    {"name": "동물원 구경하기", "icon": "🦁", "desc": "귀여운 동물들 만나고 둘러보기"},
    {"name": "수목원 나들이", "icon": "🌲", "desc": "자연 속 산림욕하며 마음의 평화 찾기"},
    {"name": "드라이브 가기", "icon": "🚗", "desc": "외곽으로 도로 타고 드라이브하기"},
    {"name": "전통시장 탐방", "icon": "🍡", "desc": "시장의 다채로운 먹거리 도장깨기"},
    {"name": "전망대 올라가기", "icon": "🏙️", "desc": "타워 전망대에서 도시 야경 관람"},
    {"name": "야구장 직관", "icon": "⚾", "desc": "응원가 부르며 치맥 먹고 직관하기"},
    {"name": "축구장 직관", "icon": "⚽", "desc": "K리그/매치 뜨거운 열기 직접 느끼기"},
    {"name": "한강 오리배 타기", "icon": "🦆", "desc": "수상 레저나 오리배 경험해보기"},
    {"name": "케이블카 타기", "icon": "🚡", "desc": "산이나 바다 위 케이블카 감상"},
    {"name": "바다 보러 떠나기", "icon": "🌊", "desc": "동해/서해 바닷가 파도 소리 듣기"},
    {"name": "유람선 타기", "icon": "🚢", "desc": "선상 투어하며 힐링하기"},
    {"name": "야경 명소 가기", "icon": "✨", "desc": "밤하늘 야경 스팟 투어하기"},
    {"name": "플리마켓 구경", "icon": "🛍️", "desc": "핸드메이드 소품과 예술품 구경"},
    {"name": "아웃렛 쇼핑", "icon": "🛍️", "desc": "쇼핑몰 거닐며 옷 구경하고 득템하기"},

    # 문화/예술
    {"name": "미술관 전시회 관람", "icon": "🖼️", "desc": "그림과 작품 감상하며 사색하기"},
    {"name": "박물관 탐방", "icon": "🏛️", "desc": "역사와 유물 둘러보기"},
    {"name": "연극 관람", "icon": "🎭", "desc": "대학로 소극장 연극 경험하기"},
    {"name": "뮤지컬 관람", "icon": "💃", "desc": "화려한 무대와 노래 감상하기"},
    {"name": "콘서트 관람", "icon": "🎶", "desc": "좋아하는 가수 라이브 공연 즐기기"},
    {"name": "영화관 영화 관람", "icon": "🍿", "desc": "최신 개봉작 팝콘 먹으며 보기"},
    {"name": "클래식/오케스트라 관람", "icon": "🎻", "desc": "웅장한 웅변과 오케스트라 청음"},
    {"name": "천문대 별자리 관측", "icon": "🌌", "desc": "망원경으로 혜성과 별 관측하기"},
    {"name": "도자기 공예 체험", "icon": "🏺", "desc": "물레 굴려 나만의 도자기 만들기"},
    {"name": "가죽 공예 체험", "icon": "👛", "desc": "지갑이나 키링 손수 제작하기"},
    {"name": "반지 만들기 체험", "icon": "💍", "desc": "커플링이나 은반지 만들기"},
    {"name": "향수 공방 가기", "icon": "🧪", "desc": "나만의 시그니처 조향 향수 제작"},
    {"name": "네온사인 DIY 체험", "icon": "💡", "desc": "화려한 네온 조명 인테리어 제작"},
    {"name": "드로잉 카페 가기", "icon": "🎨", "desc": "캔버스에 아크릴 물감으로 그림 그리기"},
    {"name": "터프팅 공방 체험", "icon": "🧶", "desc": "실로 짜는 터프팅 러그 제작"},
    {"name": "캔들/비누 만들기", "icon": "🕯️", "desc": "향기로운 천연 비누와 캔들 공예"},
    {"name": "원예/플라워 클래스", "icon": "💐", "desc": "예쁜 꽃꽂이 및 화분 만들기"},
    {"name": "쿠킹 클래스 참여", "icon": "🍳", "desc": "새로운 고급 요리 레시피 배우기"},
    {"name": "베이킹 클래스 참여", "icon": "🧁", "desc": "디저트나 케이크 직접 제과하기"},
    {"name": "목공 공예 체험", "icon": "🪵", "desc": "원목 도마나 소가구 만들기"},

    # 힐링/집/자기계발
    {"name": "찜질방/사우나 가기", "icon": "♨️", "desc": "따뜻하게 땀 빼고 식혜 마시기"},
    {"name": "마사지 받기", "icon": "💆‍♂️", "desc": "지친 몸의 피로 싹 풀어주기"},
    {"name": "스파 체험하기", "icon": "🛁", "desc": "고급 스파에서 입욕과 힐링하기"},
    {"name": "집에서 요리 도전", "icon": "👨‍🍳", "desc": "평소 안 해본 레시피로 요리하기"},
    {"name": "다이어리 꾸미기", "icon": "✏️", "desc": "다꾸용 스티커와 색펜으로 일기 쓰기"},
    {"name": "레고 조립하기", "icon": "🧱", "desc": "집중해서 디테일한 레고 완성하기"},
    {"name": "퍼즐 맞추기", "icon": "🧩", "desc": "1000피스 직소 퍼즐 완성에 도전"},
    {"name": "나노블럭/프라모델 조립", "icon": "🤖", "desc": "건담이나 미니어처 프라모델 만들기"},
    {"name": "밀린 독서하기", "icon": "📚", "desc": "사놓고 안 읽은 소설책 정독하기"},
    {"name": "뜨개질/자수 놓기", "icon": "🧶", "desc": "목도리나 수세미 짜며 집중하기"},
    {"name": "외국어 공부하기", "icon": "🗣️", "desc": "회화나 자격증 공부 자기계발"},
    {"name": "악기 연습하기", "icon": "🎸", "desc": "기타나 피아노 연주 곡 하나 마스터"},
    {"name": "블로그/글 쓰기", "icon": "💻", "desc": "나만의 일상과 지식 기록하기"},
    {"name": "홈카페 메뉴 만들기", "icon": "🍹", "desc": "예쁜 음료나 홈카페 라떼 조제"},
    {"name": "집 대청소 및 방 꾸미기", "icon": "🧹", "desc": "가구 배치 바꾸고 상쾌하게 청소"},
    {"name": "반려식물 분갈이하기", "icon": "🪴", "desc": "초록 식물 잎 닦아주고 관리하기"},
    {"name": "보드게임 혼자 플레이", "icon": "🃏", "desc": "1인 보드게임이나 퍼즐 게임하기"},
    {"name": "콘솔 게임 플레이", "icon": "🎮", "desc": "닌텐도 스위치/PS5 엔딩 보기"},
    {"name": "명상 및 음악 감상", "icon": "🎧", "desc": "헤드폰 끼고 고음질 힐링 음악 청음"},
    {"name": "가계부/재테크 정리", "icon": "💰", "desc": "월 예산 결산 및 투자 공부하기"}
]

# 4. 추천 아이디어 파트
st.subheader("2. 추천 아이디어 둘러보기")

if option == "🍱 오늘 먹거리 (100종 데이터)":
    st.info("💡 100가지 음식 중 무작위 3개를 추천해 드립니다. 담고 싶은 메뉴를 체크해 보세요!")
    
    rec_col1, rec_col2 = st.columns([3, 1])
    with rec_col2:
        if st.button("🔄 다른 먹거리 3개 추천") or not st.session_state.food_sample:
            st.session_state.food_sample = random.sample(FOOD_100, k=3)
            
    selected_foods_to_add = []
    cols = st.columns(3)
    
    for idx, food_name in enumerate(st.session_state.food_sample):
        with cols[idx]:
            st.markdown(f"### 🍽️ {food_name}")
            if st.checkbox(f"후보로 선택", key=f"chk_food_{idx}_{food_name}"):
                selected_foods_to_add.append(food_name)

    st.write("")
    if st.button("➕ 선택한 음식만 후보 목록에 담기"):
        if selected_foods_to_add:
            current_list = [x.strip() for x in st.session_state.candidates_text.split(",") if x.strip()]
            for item in selected_foods_to_add:
                if item not in current_list:
                    current_list.append(item)
            st.session_state.candidates_text = ", ".join(current_list)
            st.success(f"선택한 [{', '.join(selected_foods_to_add)}] 항목이 후보 목록에 추가되었습니다!")
        else:
            st.warning("⚠️ 담을 음식을 먼저 체크박스로 선택해 주세요!")

elif option == "🎮 주말 할거리 (100종 데이터)":
    st.info("💡 100가지 주말 놀거리 중 무작위 3개를 추천해 드립니다. 하고 싶은 활동을 체크해 보세요!")
    
    rec_col1, rec_col2 = st.columns([3, 1])
    with rec_col2:
        if st.button("🔄 다른 할거리 3개 추천") or not st.session_state.act_sample:
            st.session_state.act_sample = random.sample(ACTIVITY_100, k=3)
            
    selected_acts_to_add = []
    cols = st.columns(3)
    
    for idx, item in enumerate(st.session_state.act_sample):
        with cols[idx]:
            st.markdown(f"### {item['icon']} {item['name']}")
            st.caption(item["desc"])
            if st.checkbox(f"후보로 선택", key=f"chk_act_{idx}_{item['name']}"):
                selected_acts_to_add.append(item["name"])

    st.write("")
    if st.button("➕ 선택한 할거리만 후보 목록에 담기"):
        if selected_acts_to_add:
            current_list = [x.strip() for x in st.session_state.candidates_text.split(",") if x.strip()]
            for item in selected_acts_to_add:
                if item not in current_list:
                    current_list.append(item)
            st.session_state.candidates_text = ", ".join(current_list)
            st.success(f"선택한 [{', '.join(selected_acts_to_add)}] 항목이 후보 목록에 추가되었습니다!")
        else:
            st.warning("⚠️ 담을 활동을 먼저 체크박스로 선택해 주세요!")

else:
    st.write("원하시는 후보를 아래 3번 항목에 직접 작성해 주세요.")

st.divider()

# 5. 후보 목록 설정
st.subheader("3. 룰렛 후보 목록 설정")
user_input = st.text_area(
    "후보 목록 (위에서 선택 후 담거나 직접 쉼표로 구별하여 입력):",
    value=st.session_state.candidates_text,
    placeholder="예: 제육볶음, 탁구 치기, 실내 클라이밍 (직접 수정/추가 가능)",
    height=100
)

# ---------------------------------------------------------
# 💡 능동적 카카오맵 장소 검색어 자동 추출 함수
# ---------------------------------------------------------
def get_kakao_search_keyword(activity_name):
    # 1. 100가지 주요 활동에 대한 1:1 장소 매핑 테이블
    mapping = {
        "탁구 치기": "탁구장",
        "피크닉/돗자리 나들이": "공원",
        "피크닉하기": "공원",
        "배드민턴 치기": "체육관",
        "자전거 라이딩": "자전거대여소",
        "볼링 치기": "볼링장",
        "당구/포켓볼 치기": "당구장",
        "실내 골프/스크린골프": "스크린골프장",
        "테니스/실내테니스": "테니스장",
        "실내 클라이밍": "클라이밍장",
        "방탈출 카페 가기": "방탈출카페",
        "오락실 가서 게임하기": "오락실",
        "고양이 카페 가기": "고양이카페",
        "강아지 카페 가기": "애견카페",
        "포토부스 사진 찍기": "포토부스",
        "코인노래방 가기": "코인노래방",
        "찜질방/사우나 가기": "찜질방",
        "마사지 받기": "마사지샵",
        "영화관 영화 관람": "영화관",
        "밀린 OTT 보기": "영화관",
        "카페 가서 공부": "스터디카페",
        "침대와 일체화": "만화카페",
        "친구 만나기": "보드게임카페",
        "운동하기": "헬스장",
        "산책하기": "공원",
        "등산하기": "등산로",
        "와인바 탐방": "와인바",
        "칵테일바 가기": "칵테일바",
        "미술관 전시회 관람": "미술관",
        "박물관 탐방": "박물관",
        "연극 관람": "소극장",
        "뮤지컬 관람": "공연장",
        "수영하기": "수영장",
        "스케이트 타기": "아이스링크",
        "풋살하기": "풋살장",
        "농구하기": "농구장",
        "아쿠아리움 방문": "아쿠아리움",
        "동물원 구경하기": "동물원",
        "수목원 나들이": "수목원",
        "전통시장 탐방": "전통시장",
        "전망대 올라가기": "전망대",
        "도자기 공예 체험": "도자기공방",
        "가죽 공예 체험": "가죽공방",
        "향수 공방 가기": "향수공방",
        "드로잉 카페 가기": "드로잉카페"
    }
    
    if activity_name in mapping:
        return mapping[activity_name]
    
    # 2. 매핑 테이블에 없을 경우 문구에서 동사/조사를 제거하고 핵심 장소 명사만 능동적 추출
    keyword = activity_name
    # 서술어 및 조동사 제거
    keyword = re.sub(r'(가기|치기|하기|타기|구경하기|보기|받기|놀기|가서|만나기|탐방|관람|체험|조립하기|맞추기|만들기|꾸미기|쓰기|연습하기)$', '', keyword).strip()
    keyword = re.sub(r'(에서|으로|로|을|를|과|와|에|의)$', '', keyword).strip()
    
    # 만약 정제 후에도 문자열이 너무 길거나 상징어라면 기본 '맛집' 또는 '카페' 처리
    return keyword if len(keyword) > 0 else activity_name

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
            
            # 능동적 장소 키워드 추출
            search_keyword = get_kakao_search_keyword(selected)
            search_query = f"{location} {search_keyword}"
            encoded_query = urllib.parse.quote(search_query)
            map_url = f"https://map.kakao.com/link/search/{encoded_query}"
            
            st.balloons()
            st.success("🎉 결정 완료!")
            st.markdown(f"### 📍 현재 위치: **{location}**")
            st.markdown(f"### 👑 오늘 당신의 선택은: **[{selected}]** 입니다!")
            
            st.markdown(f"👉 [🔍 '{location} {search_keyword}' 카카오맵에서 검색하기]({map_url})")
            st.info(f"💡 팁: '{selected}' 문구를 능동적으로 인식하여 카카오맵 장소 키워드 **[{search_keyword}]**(으)로 정밀 검색했습니다.")
