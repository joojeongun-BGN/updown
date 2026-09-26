import random
import streamlit as st

# 모바일 화면 최적화 설정
st.set_page_config(page_title="100 KRW", page_icon="💰", layout="centered")

# Custom CSS: 모바일 반응형 UI 스타일링
st.markdown("""
    <style>
    .game-title { text-align: center; font-size: 26px; font-weight: bold; color: #2C3E50; margin-bottom: 5px; }
    .character { font-size: 60px; text-align: center; }
    .status-card { background-color: #F8F9F9; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid #E5E8E8; }
    .money-text { font-size: 24px; font-weight: bold; color: #27AE60; }
    .clear-text { font-size: 36px; font-weight: bold; color: #2980B9; text-align: center; animation: blink 1s infinite; }
    .gameover-text { font-size: 32px; font-weight: bold; color: #C0392B; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='game-title'>🧹 유여사의 100만원 모으기 💰</div>", unsafe_allow_html=True)

# 1. 게임 세션 상태 초기화 (충돌 방지를 위해 falling_items로 변경)
if 'money' not in st.session_state:
    st.session_state.money = 0
if 'position' not in st.session_state:
    st.session_state.position = 2  # 0~4 (총 5개 라인 중 중앙)
if 'game_status' not in st.session_state:
    st.session_state.game_status = 'PLAYING' # PLAYING, CLEAR, GAMEOVER
if 'falling_items' not in st.session_state:
    st.session_state.falling_items = [None] * 5  # 5개 라인의 떨어지는 아이템

def reset_game():
    st.session_state.money = 0
    st.session_state.position = 2
    st.session_state.game_status = 'PLAYING'
    st.session_state.falling_items = [None] * 5

# 2. 게임 진행 (한 타임스텝 진행)
def next_turn(move_dir=0):
    if st.session_state.game_status != 'PLAYING':
        return
    
    # 위치 이동 (0~4 범위 제한)
    st.session_state.position = max(0, min(4, st.session_state.position + move_dir))
    
    # 새로운 아이템 생성 (만 원, 5만 원, 돌, 빈 공간)
    new_items = []
    types = ['💵1만', '💶5만', '🪨돌', '✨빈공간', '✨빈공간']
    for _ in range(5):
        new_items.append(random.choice(types))
    st.session_state.falling_items = new_items
    
    # 현재 유여사 위치의 아이템 판정
    current_item = st.session_state.falling_items[st.session_state.position]
    
    if current_item == '💵1만':
        st.session_state.money += 10000
    elif current_item == '💶5만':
        st.session_state.money += 50000
    elif current_item == '🪨돌':
        st.session_state.game_status = 'GAMEOVER'
    
    # 100만원 달성 체크
    if st.session_state.money >= 1000000 and st.session_state.game_status != 'GAMEOVER':
        st.session_state.game_status = 'CLEAR'

# --- 상단 현재 상태 표시 ---
col_score, col_status = st.columns(2)
with col_score:
    st.markdown(f"<div class='status-card'>현재 모은 돈<br><span class='money-text'>{st.session_state.money:,} 원</span></div>", unsafe_allow_html=True)
with col_status:
    progress = min(1.0, st.session_state.money / 1000000)
    st.write("목표 달성도 (100만원)")
    st.progress(progress)

st.write("")

# --- 게임 필드 화면 그리기 ---
field_cols = st.columns(5)
for i in range(5):
    with field_cols[i]:
        # 떨어지는 아이템 표시
        item = st.session_state.falling_items[i]
        if item and item != '✨빈공간':
            st.markdown(f"<h3 style='text-align: center;'>{item}</h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='text-align: center;'>&nbsp;</h3>", unsafe_allow_html=True)
            
        # 유여사 캐릭터 표시 (파마머리/집안일 유여사 👩‍🦱🧹)
        if i == st.session_state.position:
            st.markdown("<div class='character'>👩‍🦱🧹</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-weight:bold; color:#E67E22;'>[유여사]</p>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='character'>&nbsp;</div>", unsafe_allow_html=True)

# --- 클리어 및 게임오버 상태 처리 ---
if st.session_state.game_status == 'CLEAR':
    st.balloons()
    st.markdown("<div class='clear-text'>🎉 CLEAR! 🎉</div>", unsafe_allow_html=True)
    st.success("축하합니다! 유여사가 무사히 100만원을 다 모았습니다! 🧹💰")
elif st.session_state.game_status == 'GAMEOVER':
    st.markdown("<div class='gameover-text'>💥 GAME OVER 💥</div>", unsafe_allow_html=True)
    st.error("앗! 유여사가 돌에 맞았습니다! 다시 도전해보세요.")

# --- 모바일 터치 조작 버튼 ---
st.write("---")
st.caption("📱 휴대폰 조작: 손가락으로 왼쪽/우측 버튼을 터치하여 돌을 피하고 돈을 받으세요!")

btn_col1, btn_col2, btn_col3 = st.columns([2, 3, 2])

with btn_col1:
    if st.button("👈 왼쪽 이동", use_container_width=True, disabled=(st.session_state.game_status != 'PLAYING')):
        next_turn(-1)
        st.rerun()

with btn_col2:
    if st.button("🏃 앞으로 (제자리)", use_container_width=True, disabled=(st.session_state.game_status != 'PLAYING')):
        next_turn(0)
        st.rerun()

with btn_col3:
    if st.button("오른쪽 이동 👉", use_container_width=True, disabled=(st.session_state.game_status != 'PLAYING')):
        next_turn(1)
        st.rerun()

# 재시작 버튼
if st.session_state.game_status != 'PLAYING':
    st.write("")
    if st.button("🔄 게임 다시 하기", use_container_width=True):
        reset_game()
        st.rerun()