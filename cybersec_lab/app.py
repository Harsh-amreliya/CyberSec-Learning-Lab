import streamlit as st
from utils.auth import init_auth, login_user, logout_user
from database.db import init_db

st.set_page_config(
    page_title="CyberSec Learning Lab",
    page_icon="🛡️",
    layout="wide"
)

init_auth()

def main():
    if not st.session_state['authentication_status']:
        st.title("🛡️ CyberSec Learning Lab")
        st.markdown("""
        ### Master Ethical Hacking through Hands-on Practice
        Welcome to the **CyberSec Learning Lab**, a Master's-level educational platform designed to teach you cybersecurity through
        **Problem-Based Learning** and **Scaffolded Instruction**.

        **What you will learn:**
        - Identify real-world vulnerabilities in code.
        - Craft exploits to understand the impact.
        - Implement robust patches to secure the application.
        - Explain the underlying security principles.

        **Features:**
        - **AI-Powered Evaluation:** Receive instant feedback and hints from Claude API.
        - **15+ Challenges:** From SQL Injection to Race Conditions.
        - **Gamified Learning:** Earn points, unlock badges, and climb the leaderboard.
        - **Adaptive Learning:** Get recommendations based on your performance.

        Please **Login** or **Register** in the sidebar to begin your journey.
        """)
        login_user()
    else:
        st.title(f"Welcome back, {st.session_state['username']}! 🛡️")
        st.markdown("""
        Use the sidebar to navigate through the platform:
        - **Dashboard:** View your progress, badges, and skill visualization.
        - **Challenges:** Browse and select your next challenge.
        - **Lab:** Your active workspace for solving the current challenge.
        - **Leaderboard:** See how you rank against other students.
        """)

        # Quick stats
        from database.db import query_db
        user_id = st.session_state['user_id']
        stats = query_db("SELECT total_points, (SELECT COUNT(*) FROM progress WHERE user_id = ? AND completed = 1) as completed FROM users WHERE id = ?", (user_id, user_id), one=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Points", stats['total_points'])
        col2.metric("Challenges Completed", stats['completed'])

        rank = query_db("SELECT COUNT(*) + 1 as rank FROM users WHERE total_points > ?", (stats['total_points'],), one=True)
        col3.metric("Rank", f"#{rank['rank']}")

        logout_user()

if __name__ == "__main__":
    init_db()
    main()
