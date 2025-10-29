import streamlit as st
import base64

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

col1, col2 = st.columns([2, 1]) # Adjust ratios for desired spacing

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
