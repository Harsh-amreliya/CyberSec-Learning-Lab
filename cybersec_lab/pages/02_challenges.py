import streamlit as st
from database.db import get_all_challenges, query_db
from utils.auth import init_auth

st.set_page_config(page_title="Challenges", page_icon="🧩", layout="wide")
init_auth()

if not st.session_state.get('authentication_status'):
    st.warning("Please login to view challenges.")
    st.stop()

st.title("🧩 Cybersecurity Challenges")

# Filter by category
categories = ["All"] + [c['category'] for c in query_db("SELECT DISTINCT category FROM challenges")]
selected_cat = st.selectbox("Filter by Category", categories)

challenges = get_all_challenges()

if selected_cat != "All":
    challenges = [c for c in challenges if c['category'] == selected_cat]

# Display challenges in a grid
user_id = st.session_state['user_id']
progress_data = query_db("SELECT challenge_id, completed, current_stage FROM progress WHERE user_id = ?", (user_id,))
progress_dict = {p['challenge_id']: p for p in progress_data}

cols = st.columns(3)
for i, chal in enumerate(challenges):
    with cols[i % 3]:
        prog = progress_dict.get(chal['id'])
        is_completed = prog['completed'] if prog else False
        current_stage = prog['current_stage'] if prog else 1

        status = "✅ Completed" if is_completed else f"🕒 Stage {current_stage}/4"

        st.markdown(f"### {chal['title']}")
        st.write(f"**Category:** {chal['category']}")
        st.write(f"**Difficulty:** {chal['difficulty']}")
        st.write(f"**Points:** {chal['base_points']}")
        st.write(f"**Status:** {status}")

        if st.button("Enter Lab", key=f"btn_{chal['id']}"):
            st.session_state['current_challenge_id'] = chal['id']
            st.switch_page("pages/03_lab.py")
        st.markdown("---")
