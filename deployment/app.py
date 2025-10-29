import streamlit as st
import base64
import time
from scripts.validate_customer import is_valid_customer
from agent.sql_agent import order_query_tool_func
from agent.chat_agent import answer_tool_func

# --- App Configuration ---
st.set_page_config(page_title="FoodHub Chatbot", page_icon="🍽️", layout="centered")

# --- Load Local JPG Background Image ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

image_base64 = get_base64_image("foodhub_background_jpg.jpg")  # Make sure this file exists

# --- Inject CSS for Background ---
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{image_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .right-align-container {{
        display: flex;
        justify-content: flex-end;
        padding-right: 80px;
    }}
    .login-box {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 30px;
        border-radius: 10px;
        width: 400px;
    }}
    .main > div {{
        max-width: 600px;
        margin-left: auto;
        margin-right: 0;
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 10px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

# --- Header: Logo + Title Side-by-Side ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("foodhub_logo.png", width=100)
with col2:
    st.markdown("<h1 style='color: #ff4b4b; padding-top: 10px;'>Welcome to FoodHub Chatbot</h1>", unsafe_allow_html=True)

if st.session_state.get("farewell_triggered", False):
    st.success("🙏 Thank you for chatting with FoodHub! Redirecting you to the login page…")
    time.sleep(2.5)
    st.session_state.authenticated = False
    st.session_state.customer_id = None
    st.session_state.chat_history = []
    st.session_state.farewell_triggered = False
    st.rerun()

# --- Login Page ---
if not st.session_state.authenticated:
    st.markdown('<div class="right-align-container"><div class="login-box">', unsafe_allow_html=True)
    with st.form("login_form"):

        customer_id = st.text_input("Customer ID", placeholder="eg: C1018")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log In")

        if submitted:
            if is_valid_customer(customer_id) and password == "foodhub123":
                st.session_state.authenticated = True
                st.session_state.customer_id = customer_id
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- Chatbot Interface ---
if st.session_state.authenticated:
    st.markdown(f"<h3 style='color:#ff4b4b;'>Hi {st.session_state.customer_id}, how can I help you today?</h3>", unsafe_allow_html=True)

    # --- Display Chat History ---
    for user_label, user_msg, bot_label, bot_msg in st.session_state.chat_history:
        st.markdown(
            f"""
            <div style='text-align:right; padding:8px; margin-bottom:5px;'>
                <div style='display:inline-block; background-color:#f0f0f0; color:#333; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    {user_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div style='text-align:left; padding:8px; margin-bottom:15px;'>
                <div style='display:inline-block; background-color:#ff4b4b; color:#fff; padding:10px 15px; border-radius:15px; max-width:70%;'>
                    {bot_msg}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- Clear input if flagged ---
    if st.session_state.clear_input:
        st.session_state.chat_input = ""
        st.session_state.clear_input = False

    # --- Handle input on Enter ---
    def handle_input():
      user_input = st.session_state.chat_input
      exit_keywords = ["exit", "quit", "stop", "bye", "goodbye", "end"]

      if any(keyword in user_input.lower() for keyword in exit_keywords):
          st.session_state.farewell_triggered = True
          st.session_state.chat_input = ""
      else:
          raw = order_query_tool_func(st.session_state.customer_id, user_input)
          final = answer_tool_func(raw)
          st.session_state.chat_history.append(("You", user_input, "Bot", final))
          st.session_state.clear_input = True

    # --- Chat Prompt at Bottom ---
    col1, col2 = st.columns([6, 1])
    with col1:
        st.text_input(
            "",
            placeholder="Type your message here.",
            key="chat_input",
            on_change=handle_input
        )
    with col2:
        st.markdown("<div style='padding-top: 22px;'></div>", unsafe_allow_html=True)  # Align button vertically
        if st.button("📤", help="Send"):
            handle_input()
