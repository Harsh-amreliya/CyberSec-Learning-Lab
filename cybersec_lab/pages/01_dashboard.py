import streamlit as st
import plotly.express as px
import pandas as pd
from database.db import query_db, get_user_badges
from utils.auth import init_auth
from utils.quiz import pre_post_quiz

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
init_auth()

if not st.session_state.get('authentication_status'):
    st.warning("Please login to view your dashboard.")
    st.stop()

user_id = st.session_state['user_id']
username = st.session_state['username']

st.title(f"📊 Dashboard - {username}")

# Pre/Post Quiz Integration
pre_post_quiz()

# Load User Stats
stats = query_db("""
    SELECT total_points,
    (SELECT COUNT(*) FROM progress WHERE user_id = ? AND completed = 1) as completed_challenges,
    (SELECT COUNT(*) FROM user_badges WHERE user_id = ?) as badges_earned
    FROM users WHERE id = ?
""", (user_id, user_id, user_id), one=True)

col1, col2, col3 = st.columns(3)
col1.metric("Points", stats['total_points'])
col2.metric("Challenges Completed", stats['completed_challenges'])
col3.metric("Badges Earned", stats['badges_earned'])

# Category Skill Visualization (Radar Chart)
st.subheader("🎯 Skill Proficiency")
skill_data = query_db("""
    SELECT c.category, SUM(s.ai_score) as skill_score
    FROM challenges c
    JOIN submissions s ON c.id = s.challenge_id
    WHERE s.user_id = ?
    GROUP BY c.category
""", (user_id,))

if skill_data:
    df = pd.DataFrame(skill_data)
    fig = px.line_polar(df, r='skill_score', theta='category', line_close=True)
    fig.update_traces(fill='toself')
    st.plotly_chart(fig)
else:
    st.info("Complete some challenges to see your skill visualization!")

# Progress Tracking
st.subheader("📈 Recent Activity")
activity = query_db("""
    SELECT c.title, s.stage, s.ai_score, s.created_at
    FROM submissions s
    JOIN challenges c ON s.challenge_id = c.id
    WHERE s.user_id = ?
    ORDER BY s.created_at DESC
    LIMIT 5
""", (user_id,))

if activity:
    st.table(pd.DataFrame(activity))
else:
    st.write("No recent activity.")

# Badges
st.subheader("🎖️ Your Badges")
badges = get_user_badges(user_id)
if badges:
    cols = st.columns(len(badges) if len(badges) < 5 else 5)
    for i, badge in enumerate(badges):
        with cols[i % 5]:
            st.info(f"**{badge['name']}**\n\n{badge['description']}")
else:
    st.write("Keep hacking to earn badges!")

# Adaptive Recommendations
from utils.scoring import get_recommendations
st.subheader("🚀 Recommended for You")
recs = get_recommendations(user_id)
if recs:
    for rec in recs:
        with st.expander(f"{rec['title']} ({rec['category']})"):
            st.write(rec['description'])
            if st.button(f"Start {rec['id']}", key=f"rec_{rec['id']}"):
                st.session_state['current_challenge_id'] = rec['id']
                st.switch_page("pages/03_lab.py")
