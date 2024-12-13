import streamlit as st
import random

def init_session_state():
    if 'survival_score' not in st.session_state:
        st.session_state.survival_score = 5000  # 생존 점수 초기값
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'history' not in st.session_state:
        st.session_state.history = []

def get_scenario(scenario_num):
    scenarios = [
        {
            "title": "급박한 피난 상황",
            "image": "피난.jpg",
            "description": "1950년 6월 25일, 새벽에 갑작스러운 포성 소리에 잠에서 깼습니다. 북한군이 남하중이라는 소식입니다. 단 10분 안에 집을 떠나야 합니다. 무엇을 챙기시겠습니까?",
            "choices": {
                "따뜻한 옷과 담요": {"score": 500, "message": "추운 날씨를 견딜 수 있는 현명한 선택이었습니다."},
                "귀중품과 현금": {"score": 500, "message": "피난 생활에 필요한 물건을 살 수 있게 되었습니다."},
                "가족사진과 도장": {"score": -500, "message": "실용적이지 않은 선택이었습니다."},
                "쌀과 물": {"score": 1000, "message": "가장 기본적인 생존 물품을 챙기셨습니다."}
            }
        },
        {
            "title": "서울 함락 직전",
            "image": "서울함락.jpg",
            "description": "6월 28일, 서울이 곧 함락될 것 같습니다. 정부는 이미 대전으로 피난했다고 합니다. 어떻게 하시겠습니까?",
            "choices": {
                "한강을 건너 남쪽으로 피난한다": {"score": 1000, "message": "힘들지만 안전한 선택입니다."},
                "숨어서 북한군이 지나가기를 기다린다": {"score": -10000, "message": "앗! 북한군에게 잡혔습니다."},
                "가족과 함께 농촌으로 피난한다": {"score": 500, "message": "일시적으로 안전할 수 있지만, 장기적으로는 불확실합니다."},
                "국군에 자원입대한다": {"score": 0, "message": "병든 어머니를 두고 입대할 수 없습니다."}
            }
        },
        {
            "title": "낙동강 방어선",
            "image": "낙동강방어선.jpg",
            "description": "8월 1일, 북한군의 공세에 밀려 국군과 유엔군이 낙동강 방어선을 구축했습니다. 어떤 선택을 하시겠습니까?",
            "choices": {
                "전선 가까이 피난간다": {"score": -10000, "message": "전선은 전쟁이 벌어지는 맨 앞 지역을 의미합니다.왜 위험한 곳으로 가시나요?"},
                "피난민 수용소에서 지낸다": {"score": 0, "message": "최소한의 의식주는 해결되지만, 열악한 환경입니다."},
                "일본으로의 밀항을 시도한다": {"score": -10000, "message": "매우 위험하고 불법적인 선택입니다."},
                "전선에서 최대한 멀리 떨어진 곳으로 무작정 이동한다": {"score": 1000, "message": "국군과 유엔군의 도움을 받아 최대한 전선으로부터 멀리 이동하였습니다."}
            }
        },
        {
            "title": "인천상륙작전",
            "image": "인천상륙작전.jpg",
            "description": "9월 15일, 인천상륙작전이 성공했다는 소식입니다. 서울을 다시 되찾을 희망이 생겼습니다. 어떻게 하시겠습니까?",
            "choices": {
                "서울로 즉시 돌아간다": {"score": -800, "message": "아직 전투가 진행 중이라 위험합니다."},
                "부산에서 조금 더 기다린다": {"score": 500, "message": "안전한 선택입니다."},
                "여전히 불안하므로 더 남쪽으로 이동한다": {"score": 500, "message": "안전한 선택입니다."},
                "구호물자 분배 활동에 참여한다": {"score": 800, "message": "굉장히 의미 있는 선택입니다."}
            }
        },
        {
            "title": "중공군 개입",
            "image": "중공군.jpg",
            "description": "1950년 10월 25일, 중공군이 개입했다는 소식입니다. 다시 북쪽에서 밀려오는 상황, 어떻게 대처하시겠습니까?",
            "choices": {
                "서울에서 버틴다": {"score": -10000, "message": "매우 위험한 선택입니다."},
                "다시 남쪽으로 피난한다": {"score": 1000, "message": "힘들지만 안전한 선택입니다."},
                "산속에 은신처를 만든다": {"score": 0, "message": "위험하지만 운이 좋다면 살아남을 수 있습니다."},
                "유엔군 부대에 협력을 요청한다": {"score": 500, "message": "도움을 받을 수 있지만, 유엔군도 후퇴 중입니다."}
            }
        },
        {
            "title": "1·4 후퇴",
            "image": "14후퇴.jpg",
            "description": "1951년 1월 4일, 서울이 다시 함락되었습니다. 한겨울에 피난길에 오른 당신, 어떤 선택을 하시겠습니까?",
            "choices": {
                "걸어서 남쪽으로 이동한다": {"score": 500, "message": "느리지만 확실한 방법입니다."},
                "열차를 타려고 기차역으로 간다": {"score": 200, "message": "운이 좋다면 빠르게 이동할 수 있지만, 매우 혼잡합니다."},
                "유엔군 트럭에 동승을 요청한다": {"score": 1000, "message": "가장 빠르고 안전한 방법입니다."},
                "근처 마을에서 피난처를 찾는다": {"score": -500, "message": "임시방편일 뿐, 계속 위험할 수 있습니다."}
            }
        },
        {
            "title": "제네바 협정",
            "image": "휴전협정.jpg",
            "description": "1953년 7월 27일, 제네바 협정으로 휴전이 성립되었습니다. 이제 어떤 선택을 하시겠습니까?",
            "choices": {
                "고향으로 돌아간다": {"score": 500, "message": "위험할 수 있지만, 고향을 재건할 수 있습니다."},
                "현재 거주지에 정착한다": {"score": 1000, "message": "안정적인 선택입니다."},
                "북쪽에 있는 가족을 찾아 나선다": {"score": -10000, "message": "38도선을 넘어가는 것은 불가능합니다."},
                "해외 이주를 고려한다": {"score": -500, "message": "새로운 시작일 수 있지만, 많은 어려움이 따를 것입니다."}
            }
        }
    ]
    return scenarios[scenario_num] if scenario_num < len(scenarios) else None

def show_game():
    st.title("6.25 전쟁 피난민 생존기")
    
    # 현재 생존 점수 표시
    st.sidebar.metric("생존 점수", st.session_state.survival_score)
    
    # 게임 오버 체크
    if st.session_state.survival_score <= 0:
        st.session_state.game_over = True
    
    if st.session_state.game_over:
        st.error("게임 오버! 생존에 실패했습니다.")
        if st.button("다시 시작"):
            st.session_state.clear()
            st.rerun()
        return

    # 현재 시나리오 가져오기
    scenario = get_scenario(st.session_state.current_scenario)
    
    if scenario is None:
        st.success(f"축하합니다! 피난 성공했습니다. 최종 생존 점수: {st.session_state.survival_score}")
        if st.button("다시 시작"):
            st.session_state.clear()
            st.rerun()
        return

    st.header(scenario["title"])
    
    # 이미지가 있는 경우 표시
    if "image" in scenario and scenario["image"]:
        st.image(scenario["image"], caption=scenario["title"])
    
    st.write(scenario["description"])
    
    # 선택지 제공
    choice = st.radio("선택하세요:", list(scenario["choices"].keys()), key=f"scenario_{st.session_state.current_scenario}")
    
    if st.button("선택 완료", key="choice_confirm_btn"):
        result = scenario["choices"][choice]
        st.session_state.survival_score += result["score"]
        st.session_state.history.append(f"{scenario['title']}: {choice} ({result['message']})")
        
        # 결과 메시지 표시
        if result["score"] > 0:
            st.success(f"{result['message']} (점수 +{result['score']})")
        else:
            st.error(f"{result['message']} (점수 {result['score']})")
        
        st.session_state.current_scenario += 1
        st.rerun()

    # 지난 선택 히스토리 표시
    if st.session_state.history:
        st.sidebar.header("지난 선택들")
        for event in st.session_state.history:
            st.sidebar.write(event)

def main():
    st.markdown(
        """
        <style>
        .main {
            background-color: white;
            color: black !important;
        }
        .stButton > button {
            color: black;
            background-color: transparent;
            border: 1px solid white;
        }
        .stButton > button:hover {
            color: white;
            background-color: black;
        }
        .stRadio > label {
            color: black !important;
        }
        .stMarkdown {
            color: black !important;
        }
        .stTitle {
            color: black !important;
        }
        .stHeader {
            color: black !important;
        }
        div[data-testid="stMetricValue"] {
            color: black !important;
        }
        div[data-testid="stMetricLabel"] {
            color: black !important;
        }
        .stSidebar {
            background-color: black;
        }
        .stSidebar [data-testid="stMarkdown"] {
            color: white !important;
        }
        .stSidebar [data-testid="stHeader"] {
            color: white !important;
        }
        .stSidebar [data-testid="stMetricValue"] {
            color: white !important;
        }
        .stSidebar [data-testid="stMetricLabel"] {
            color: white !important;
        }
        /* 추가된 스타일 */
        p {
            color: white !important;
        }
        h1, h2, h3 {
            color: white !important;
        }
        .stRadio label span {
            color: white !important;
        }
        div[data-baseweb="radio"] {
            color: white !important;
        }
        .element-container {
            color: white !important;
        }
        /* 사이드바 스타일 수정 */
        section[data-testid="stSidebar"] {
            background-color: black !important;
        }
        section[data-testid="stSidebar"] > div {
            background-color: black !important;
        }
        section[data-testid="stSidebar"] .stMarkdown {
            color: white !important;
        }
        /* 기본 버튼 스타일 */
        .stButton > button {
            color: white;
            background-color: transparent;
            border: 1px solid white;
        }
        
        /* 일반 버튼 호버 효과 */
        .stButton > button:hover {
            color: black;
            background-color: white;
        }
        
        /* 선택완료 버튼 스타일 */
        button[kind="secondary"] {
            color: orange !important;
        }
        
        /* 선택완료 버튼 호버 효과 */
        button[kind="secondary"]:hover {
            color: black !important;
            background-color: orange !important;
            border-color: orange !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    init_session_state()
    show_game()

if __name__ == "__main__":
    main()
