import streamlit as st
import base64
from validate_customer import is_valid_customer

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
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

#if not st.session_state.authenticated:
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
   """,
   unsafe_allow_html=True
)
#else:
    # Clear background after login
#    st.markdown(
#        """
#        <style>
#        .stApp {
#            background-image: none !important;
#            background-color: #ffffff !important;
#        }
#        </style>
#        """,
#        unsafe_allow_html=True
#    )
    

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
                #if is_valid_customer(customer_id) and password == "foodhub123":
                st.session_state.authenticated = True
                st.session_state.customer_id = customer_id
                st.session_state.chat_history = []
                st.rerun()
               # else:
               #     st.error("Invalid credentials. Please try again.")
               #     st.rerun()
                
# --- Chatbot Interface ---
if st.session_state.authenticated:
    customer_id = st.session_state.get("customer_id")
    col1, col2 = st.columns([1, 3])
    # Ensure chat history
    if "history" not in st.session_state:
        st.session_state["history"] = [
            {"role": "assistant", "content": f"Hi {customer_id or 'there'}! How can I help you today?"}
        ]
    with col2:
        st.subheader(f"Welcome {customer_id} to FoodHub Chatbot")
        # Chat input
        for m in st.session_state.history:
            with st.chat_message("user" if m["role"]=="user" else "assistant"):
                bubble = "chat-bubble-user" if m["role"]=="user" else "chat-bubble-bot"
                st.markdown(f"<div class='{bubble}'>{m['content']}</div>", unsafe_allow_html=True)

        # 2) input → append → bot → append → rerun
        prompt = st.chat_input("Ask about your order, offers, or menu…")
        if prompt:
            st.session_state.history.append({"role":"user","content":prompt})
            reply = "hello"                    # swap with real LLM/Agent call
            st.session_state.history.append({"role":"assistant","content":reply})
            st.rerun()
  
