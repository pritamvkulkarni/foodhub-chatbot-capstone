import streamlit as st
from agent.sql_agent import order_query_tool_func
from agent.chat_agent import answer_tool_func
from scripts.validate_customer import is_valid_customer

# --- App Configuration ---
st.set_page_config(page_title="FoodHub Chatbot", page_icon="🍽️", layout="centered")

# --- Logo and Branding ---
st.image("foodHub_logo.png", width=120)  # Replace with your logo URL
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>Welcome to FoodHub Chatbot</h1>", unsafe_allow_html=True)

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Login Page ---
if not st.session_state.authenticated:
    with st.form("login_form"):
        customer_id = st.text_input("Customer ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")

        if submitted:
            if is_valid_customer(customer_id) and password == "foodhub123":  # Replace with real auth logic
                st.session_state.authenticated = True
                st.session_state.customer_id = customer_id
                st.session_state.chat_history = []
                st.success("✅ Login successful!")
            else:
                st.error("❌ Invalid credentials. Please try again.")

# --- Chatbot Interface ---
if st.session_state.authenticated:
    st.markdown(f"<h3 style='color:#ff4b4b;'>Hi {st.session_state.customer_id}, how can I help you today?</h3>", unsafe_allow_html=True)
    user_input = st.text_input("Type your message below (type 'exit' to logout):")

    if st.button("Send") and user_input:
        if user_input.lower().strip() == "exit":
            st.info("👋 You’ve exited the chat. Please log in again to continue.")
            st.session_state.authenticated = False
            st.session_state.customer_id = None
            st.session_state.chat_history = []
            st.experimental_rerun()
        else:
            raw = order_query_tool_func(st.session_state.customer_id, user_input)
            final = answer_tool_func(raw)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", final))

    # --- Display Chat History (latest on top) ---
    for sender, message in reversed(st.session_state.chat_history):
        if sender == "You":
            st.markdown(
                f"""
                <div style='text-align:right; padding:8px; margin-bottom:10px;'>
                    <div style='display:inline-block; background-color:#f0f0f0; color:#333; padding:10px 15px; border-radius:15px; max-width:70%;'>
                        {message}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='text-align:left; padding:8px; margin-bottom:10px;'>
                    <div style='display:inline-block; background-color:#ff4b4b; color:#fff; padding:10px 15px; border-radius:15px; max-width:70%;'>
                        {message}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
