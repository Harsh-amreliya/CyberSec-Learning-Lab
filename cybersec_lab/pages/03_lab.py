import streamlit as st
import time
from database.db import get_user_progress, update_user_progress, add_submission
from challenges.challenge_loader import get_challenge_details
from ai.evaluator import evaluate_submission
from utils.auth import init_auth
from utils.scoring import calculate_points, check_badges

st.set_page_config(page_title="Lab", page_icon="🧪", layout="wide")
init_auth()

if not st.session_state.get('authentication_status'):
    st.warning("Please login to access the Lab.")
    st.stop()

challenge_id = st.session_state.get('current_challenge_id')

if not challenge_id:
    st.info("Please select a challenge from the Challenges page.")
    if st.button("Go to Challenges"):
        st.switch_page("pages/02_challenges.py")
    st.stop()

# Load challenge data
challenge = get_challenge_details(challenge_id)
user_id = st.session_state['user_id']
progress = get_user_progress(user_id, challenge_id)

if not progress:
    update_user_progress(user_id, challenge_id, 1)
    progress = get_user_progress(user_id, challenge_id)

current_stage_idx = progress['current_stage'] - 1 # 0-indexed
completed = progress['completed']

# Initialize stage timer
if 'stage_start_time' not in st.session_state or st.session_state.get('last_stage') != progress['current_stage']:
    st.session_state['stage_start_time'] = time.time()
    st.session_state['last_stage'] = progress['current_stage']

st.title(f"🧪 Lab: {challenge['title']}")
st.markdown(f"**Category:** {challenge['category']} | **Difficulty:** {challenge['difficulty']}")

# Progress bar
st.progress(progress['current_stage'] / 4)

if completed:
    st.success("🎉 You have completed this challenge!")
    if st.button("Back to Challenges"):
        st.switch_page("pages/02_challenges.py")
    # Allow re-viewing or proceed?
    # For now, let's show the final state or allow them to continue
    # Actually, let's cap it at stage 4.

if current_stage_idx < 4:
    stage = challenge['stages'][current_stage_idx]

    st.header(f"Stage {progress['current_stage']}: {stage['name']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Instructions")
        st.info(stage['instruction'])

        st.subheader("Vulnerable Code")
        st.code(challenge['vuln_code'], language='python')

    with col2:
        st.subheader("Your Submission")
        answer = st.text_area("Enter your answer or payload here:", height=150)

        # Hint system
        hints_used = progress['hints_used']
        if hints_used < 3:
            if st.button(f"Use Hint ({hints_used}/3) - Penalty Applied"):
                st.write(f"**Hint:** {challenge['hints'][hints_used]}")
                update_user_progress(user_id, challenge_id, progress['current_stage'], hints_used=1)
                st.rerun()
        else:
            st.warning("All hints used.")

        if st.button("Submit"):
            if not answer:
                st.error("Please enter an answer.")
            else:
                with st.spinner("AI is evaluating your submission..."):
                    result = evaluate_submission(challenge, current_stage_idx, answer)

                score = result['score']
                feedback = result['feedback']
                hint = result['hint']

                st.session_state['last_result'] = result

                if score >= 0.7:
                    time_taken = time.time() - st.session_state['stage_start_time']
                    points = calculate_points(challenge['base_points'], current_stage_idx, score, hints_used, progress['attempts'], time_taken=time_taken)

                    is_last_stage = (progress['current_stage'] == 4)
                    new_stage = progress['current_stage'] + (0 if is_last_stage else 1)

                    add_submission(user_id, challenge_id, progress['current_stage'], answer, score, feedback, hint, points)
                    update_user_progress(user_id, challenge_id, new_stage, completed=is_last_stage)

                    new_badges = check_badges(user_id, challenge_id, current_stage_idx, score, hints_used)
                    for b in new_badges:
                        st.balloons()
                        st.success(f"🎖️ New Badge Earned: {b}!")

                    st.success(f"Correct! Score: {score:.2f}. Points Awarded: {points}")
                    st.write(feedback)
                    st.info(f"AI Hint: {hint}")

                    time.sleep(2)
                    st.rerun()
                else:
                    add_submission(user_id, challenge_id, progress['current_stage'], answer, score, feedback, hint, 0)
                    update_user_progress(user_id, challenge_id, progress['current_stage'])
                    st.error(f"Try again. Score: {score:.2f}")
                    st.write(feedback)
                    st.info(f"AI Hint: {hint}")

else:
    st.success("Challenge Completed!")
    if st.button("Return to Challenges"):
        st.switch_page("pages/02_challenges.py")
