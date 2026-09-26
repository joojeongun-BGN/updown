import random
import streamlit as st

st.title("🎮 UP & DOWN 게임")
st.write("1부터 100 사이의 숫자를 맞혀보세요!")

if "secret" not in st.session_state:
  st.session_state.secret = random.randint(1, 100)
  st.session_state.count = 0

user_guess = st.number_input(
    "숫자 입력", min_value=1, max_value=100, step=1
)

if st.button("제출"):
  st.session_state.count += 1
  if user_guess < st.session_state.secret:
    st.warning("📈 UP!")
  elif user_guess > st.session_state.secret:
    st.warning("📉 DOWN!")
  else:
    st.success(
        f"🎉 정답입니다! ({st.session_state.count}번 만에 맞춤)"
    )
    if st.button("다시 하기"):
      st.session_state.secret = random.randint(1, 100)
      st.session_state.count = 0