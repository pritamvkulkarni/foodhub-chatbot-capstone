import streamlit as st
import base64
from validate_customer import is_valid_customer

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
col1, col2 = st.columns([2, 2]) # Adjust ratios for desired spacing

with col2:
    col1, col2 = st.columns([1, 2])
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
                st.session_state.chat_history = []
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
                
# --- Chatbot Interface ---
if st.session_state.authenticated:
    customer_id = st.session_state.get("customer_id")
    st.title("FoodHub Chatbot")
    st.subheader(f"Welcome {customer_id} to FoodHub Chatbot")

    # Ensure chat history
    if "history" not in st.session_state:
        st.session_state["history"] = [
            {"role": "assistant", "content": f"Hi {customer_id or 'there'}! How can I help you today?"}
        ]

    # Render history
    for msg in st.session_state["history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        query = st.text_area("Ask your question:", placeholder="e.g., Track my last order", height=120)
        send = st.form_submit_button("Submit")

    if send:
        if not query.strip():
            st.warning("Please enter a query before submitting.")
          
    
