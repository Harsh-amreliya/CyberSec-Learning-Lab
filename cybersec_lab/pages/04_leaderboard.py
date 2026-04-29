import streamlit as st
import pandas as pd
from database.db import get_leaderboard
from utils.auth import init_auth

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")
init_auth()

st.title("🏆 Hall of Fame")
st.markdown("Behold the top ethical hackers in the lab!")

leaderboard_data = get_leaderboard()

if leaderboard_data:
    df = pd.DataFrame(leaderboard_data)
    df.index = range(1, len(df) + 1)
    df.columns = ["Username", "Total Points", "Challenges Completed", "Badges"]

    # Highlight the current user
    def highlight_me(s):
        return ['background-color: #2e7d32' if s.Username == st.session_state.get('username') else '' for _ in s]

    st.table(df)

    # st.dataframe(df.style.apply(highlight_me, axis=1)) # st.table is often cleaner for small lists
else:
    st.info("No data available yet. Start hacking to appear on the leaderboard!")

st.subheader("How to earn points?")
st.markdown("""
- **Complete Stages:** Each stage of a challenge grants points based on AI score.
- **Perfect Score:** Get 1.0 from AI for a **+50 bonus**.
- **Speed Bonus:** Solve a stage quickly for a **+20 bonus**.
- **Hint Penalty:** Using a hint costs **-10 points**.
- **Attempt Penalty:** Multiple failed attempts cost **-5 points** each.
""")
