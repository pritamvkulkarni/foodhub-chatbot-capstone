import streamlit as st
from deployment.agent.chat_agent import order_query_tool_func, answer_tool_func
from scripts.validate_customer import is_valid_customer
import streamlit.session_state as session

st.title("FoodHub Chatbot")

# Initialize session state
if "customer_id" not in session:
    session.customer_id = None
if "chat_active" not in session:
    session.chat_active = False
if "chat_history" not in session:
    session.chat_history = []

# Step 1: Enter Customer ID
if not session.chat_active:
    customer_id_input = st.text_input("Enter your Customer ID")
    if st.button("Validate ID") and customer_id_input:
        if is_valid_customer(customer_id_input):
            session.customer_id = customer_id_input
            session.chat_active = True
            session.chat_history = []
            st.success(f"Welcome, Customer {customer_id_input}!")
        else:
            st.error("Invalid Customer ID. Please try again.")

# Step 2: Chat session
if session.chat_active:
    user_input = st.text_input("Ask about your order (type 'exit' to end)")
    if st.button("Submit") and user_input:
        if user_input.lower().strip() == "exit":
            st.info("🔚 Session ended. Please enter your Customer ID to start again.")
            session.customer_id = None
            session.chat_active = False
            session.chat_history = []
        else:
            raw = order_query_tool_func(session.customer_id, user_input)
            final = answer_tool_func(raw)
            session.chat_history.append((user_input, final))

    # Display chat history
    for query, response in session.chat_history:
        st.markdown(f"**You:** {query}")
        st.markdown(f"**Bot:** {response}")
