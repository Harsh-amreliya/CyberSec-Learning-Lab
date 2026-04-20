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

def hash_password(password):
    return stauth.Hasher.hash(password)

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
                if stauth.Hasher.check_pw(user['password_hash'], password):
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
