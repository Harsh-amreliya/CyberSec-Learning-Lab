import streamlit as st
from database.db import query_db, execute_db

def pre_post_quiz():
    st.header("📝 Knowledge Check")

    # Check if user has already taken the pre-quiz
    user_id = st.session_state['user_id']
    # We'll use a simple flag in the DB or session for this demo
    # For a Master's level, let's add a table if needed, but let's keep it simple for now

    quiz_type = "Pre-Lab" if not st.session_state.get('pre_quiz_done') else "Post-Lab"

    st.subheader(f"{quiz_type} Quiz")

    q1 = st.radio("What is the primary goal of parameterized queries?",
                  ["To make code faster", "To prevent SQL injection", "To use less memory"])

    q2 = st.radio("Which HTTP header is commonly used to prevent CSRF?",
                  ["X-Frame-Options", "X-CSRF-Token", "Content-Type"])

    if st.button(f"Submit {quiz_type}"):
        st.success(f"{quiz_type} submitted! Your progress is being tracked.")
        if quiz_type == "Pre-Lab":
            st.session_state['pre_quiz_done'] = True
        else:
            st.session_state['post_quiz_done'] = True
        st.rerun()

# This can be integrated into the Lab or a separate page
