import streamlit as st
import base64
from scripts.validate_customer import is_valid_customer

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
    

# Login form
col_left, col_right = st.columns([2, 1])

with col_right:
    # Container for logo and welcome message
    logo_col, text_col = st.columns([1, 5])
    
    with logo_col:
        st.image("foodhub_logo.png", width=60)  # Slightly smaller for better vertical alignment
    
    with text_col:
        st.markdown("""
            <h2 style='color: #ff4b4b; padding-top: 10px; margin-bottom: 0;'>Welcome to</h2>
            <h1 style='color: #ff4b4b; margin-top: 0;'>FoodHub Chatbot</h1>
        """, unsafe_allow_html=True)

    # Login form below the header
    with st.form("login_form"):
        customer_id = st.text_input("Customer ID", placeholder="eg: C1018")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if is_valid_customer(customer_id) and password == "foodhub123":
                st.session_state.authenticated = True
                st.session_state.customer_id = customer_id
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
