
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd


# 페이지 설정
st.set_page_config(
    page_title = "학생 감정기록"
)

st.title("감정일기 기록")
st.text("여러분이 오늘 느낀 감정을 알려주세요.")
st.text("그리고 감정을 느꼈던 이유, 있었던 일들을 간단하게 알려주세요.")

# --- Google Sheets 연결 설정 ---
# secrets.toml 파일에 저장된 연결 정보를 사용합니다.
# toml 파일은 키-값 구조와 간단한 문법을 가진 설정 파일 형식입니다.

conn = st.connection("gsheets", type=GSheetsConnection)

# --- 기존 데이터 읽어오기 --
# (선택사항: 데이터를 화면에 표시하고 싶을 때 사용)
# worksheet = "Sheet1"
# existing_data = conn.read(worksheet="Sheet1", usecols=list(range(4)), ttl=5)
# existing_data = existing_data.dropna(how="all")

# --- 감정 선택 옵션 ---
sentiment_options = {

    "1" : "😊기쁨",
    "2" : "😆웃김",
    "3" : "😐보통",
    "4" : "😴졸림",
    "5" : "🥺속상",
    "6" : "😠화남"

#--- 출처: emojipedia.org ---
#--- 감정이 많으면 학생들이 고르기 어려워함 ---
}

with st.form(key="emotion_form"):
    student_name = st.text_input(label="이름을 입력하세요.")
    date = st.date_input("오늘 날짜를 선택하세요.", value=None)
    selected_sentiment = st.selectbox(label="오늘 감정", options = sentiment_options.values())
    reason = st.text_area(label="감정 이유")


    submit_button = st.form_submit_button(label = "제출")
    # --- 제출 버튼을 눌렀을 때의 로직 ---
    if submit_button:
        if not student_name:
            st.error("이름을 입력해주세요.")
        elif not reason:
            st.error("**그 감정을 느낀 이유를 알려주세요.**")
        else:
            # 구글 시트에 저장할 데이터 생성

            new_data = pd.DataFrame(
                [
                    {
                        "이름": student_name,
                        "날짜": date.strftime("%Y-%m-%d"),
                        "감정": selected_sentiment,
                        "이유": reason,
                    }
                ]
            )

            updated_df = pd.concat([existing_data, new_data], ignore_index=True)

            conn.update(worksheet="daily_emotions", data=updated_df)

            st.success("오늘의 감정이 기록되었어요! 🎉")


