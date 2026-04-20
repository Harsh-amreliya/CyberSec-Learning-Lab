import streamlit as st
import streamlit_authenticator as stauth
from database.db import get_user_by_username, create_user

def init_auth():
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    if 'username' not in st.session_state:
        st.session_state['username'] = None
    if 'logout' not in st.session_state:
        st.session_state['logout'] = False

def get_authenticator():
    # In a real app, you'd load all users from the DB here
    # For Streamlit Authenticator, we need a config dictionary
    # But since we are using a DB, we can't easily use its built-in login widget
    # without syncing.
    # Let's implement a custom auth layer or use stauth with a dummy config
    # and handle the verification ourselves.

    # Actually, streamlit-authenticator 0.3.x has changed its API.
    # Let's use a simpler approach for this project if stauth is too complex for DB sync.
    # But the requirement says "Use streamlit-authenticator".

    # We will use a mock config for the Authenticator and handle the actual check manually
    # or populate it from the DB.
    pass

def hash_password(password):
    return stauth.Hasher([password]).generate()[0]

def login_user():
    st.sidebar.title("Login / Register")

    choice = st.sidebar.radio("Action", ["Login", "Register"])

    if choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.button("Login"):
            user = get_user_by_username(username)
            if user:
                # verify password
                if stauth.Hasher.verify_password(password, user['password_hash']):
                    st.session_state['authentication_status'] = True
                    st.session_state['username'] = username
                    st.session_state['user_id'] = user['id']
                    st.rerun()
                else:
                    st.error("Invalid password")
            else:
                st.error("User not found")

    else:
        new_username = st.sidebar.text_input("New Username")
        new_email = st.sidebar.text_input("Email")
        new_password = st.sidebar.text_input("New Password", type="password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password")

        if st.sidebar.button("Register"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif get_user_by_username(new_username):
                st.error("Username already exists")
            else:
                hashed = hash_password(new_password)
                create_user(new_username, new_email, hashed)
                st.success("Account created! Please login.")

def logout_user():
    if st.sidebar.button("Logout"):
        st.session_state['authentication_status'] = None
        st.session_state['username'] = None
        st.session_state['user_id'] = None
        st.rerun()
