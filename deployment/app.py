

import streamlit as st
import base64
from validate_customer import is_valid_customer
from agent.chat_agent import answer_tool_func
from agent.sql_agent import order_query_tool_func

# --- App Configuration ---
st.set_page_config(page_title="FoodHub Chatbot", page_icon="🍽️", layout="wide")

# --- Load Local JPG Background Image ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

image_base64 = get_base64_image("foodhub_background_jpg.jpg")  # Make sure this file exists

# --- Session State Initialization ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "customer_id" not in st.session_state:
    st.session_state.customer_id = None
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if not st.session_state.authenticated:
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
        </style>
       """,
       unsafe_allow_html=True
    )
else:
    # Clear background after login
    st.markdown(f"""
        <style>
        /* Remove background from stApp so blurred layer shows through */
        .stApp {{
            background-image: none !important;
            background-color: transparent !important;
        }}
        .blurred-bg {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url("data:image/jpeg;base64,{image_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            z-index: -1;
            filter: blur(6px);
        }}
        </style>
        <div class="blurred-bg"></div>
        """, 
        unsafe_allow_html=True
    )
    

if not st.session_state.authenticated:
    # Login form
    col1, col2 = st.columns([2, 2]) # Adjust ratios for desired spacing

    with col2:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image("foodhub_logo.png", width=500)
        with col2:
            st.markdown("<h1 style='color: #ff4b4b; padding-top: 10px;'>Welcome to FoodHub Chatbot</h1>", unsafe_allow_html=True)
        with st.form("login_form"):
            customer_id = st.text_input("Customer ID", placeholder="eg: C1018")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                # Add your login logic here
                if is_valid_customer(customer_id) and password == "foodhub123":
                    st.session_state.authenticated = True
                    st.session_state.customer_id = customer_id
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
                
# --- Chatbot Interface ---
if st.session_state.authenticated:
    customer_id = st.session_state.get("customer_id")
    # Ensure chat history
    if not st.session_state.chat_history:
        st.session_state["chat_history"] = [
            {"role": "assistant", "content": f"Hi! How can I help you today?"}
        ]
    spacer_left, chat_col, spacer_right = st.columns([1, 4, 1])
    
    with chat_col:
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            st.image("foodhub_logo.png", width=100)
        with col2:
            st.markdown(
                f"""
                <div style='display: flex; align-items: center; justify-content: flex-start; height: 100%;'>
                    <h1 style='color: #ff4b4b; margin: 0;'>Hey {customer_id}, Welcome!</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown("<div style='text-align: right; padding-top: 10px;'>", unsafe_allow_html=True)
            if st.button("Logout"):
                st.session_state.authenticated = False
                st.session_state.customer_id = None
                st.session_state.chat_history = []
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
                
        st.markdown("---")
        
        # Inject custom CSS for chat bubbles
        st.markdown("""
        <style>
        .chat-bubble-user {
            background-color: #dfe6e9;  /* soft gray-blue, neutral on light/dark */
            color: #000000;             /* black text */
            padding: 10px 14px;
            border-radius: 12px;
            margin-bottom: 6px;
            display: inline-block;
            max-width: 80%;
            text-align: right;
        }

        .chat-bubble-bot {
            background-color: #f1f0f0;  /* light gray, works on both themes */
            color: #000000;             /* black text */
            padding: 10px 14px;
            border-radius: 12px;
            margin-bottom: 6px;
            display: inline-block;
            max-width: 80%;
            text-align: left;
        }
        </style>
        """, unsafe_allow_html=True)

        # Chat rendering
        for m in st.session_state.chat_history:
            left_col, right_col = st.columns([1, 1])

            if m["role"] == "user":
                with right_col:
                    st.markdown(
                        f"""
                        <div style='display: flex; justify-content: flex-end; align-items: center; margin-bottom: 8px;'>
                            <div class='chat-bubble-user'>{m['content']}</div>
                            <div style='font-size: 20px; margin-left: 8px;'>🙋</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:
                with left_col:
                    st.markdown(
                        f"""
                        <div style='display: flex; justify-content: flex-start; align-items: center; margin-bottom: 8px;'>
                            <div style='font-size: 20px; margin-right: 8px;'>🤖</div>
                            <div class='chat-bubble-bot'>{m['content']}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # 2) input → append → bot → append → rerun
        prompt = st.chat_input("Ask about your order or menu...")
        if prompt:
            st.session_state.chat_history.append({"role":"user","content":prompt})
            with st.spinner("Let me check that for you..."):
                raw_response = order_query_tool_func(st.session_state.customer_id, prompt)
                reply = answer_tool_func(raw_response)
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()
