import streamlit as st

st.set_page_config(layout="wide") # Optional: Use wide layout for more space

col1, col2 = st.columns([3, 1]) # Adjust ratios for desired spacing

with col2:
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            # Add your login logic here
            if username == "user" and password == "pass":
                st.success("Logged in successfully!")
            else:
                st.error("Invalid credentials.")
