import streamlit as st
from agent.sql_agent import order_query_tool_func
from agent.chat_agent import answer_tool_func
from scripts.validate_customer import is_valid_customer

st.title("FoodHub Chatbot")

# Initialize session state
if "customer_id" not in st.session_state:
    st.session_state["customer_id"] = None
if "chat_active" not in st.session_state:
    st.session_state["chat_active"] = False
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Step 1: Enter Customer ID
if not st.session_state["chat_active"]:
    customer_id_input = st.text_input("Enter your Customer ID")
    if st.button("Validate ID") and customer_id_input:
        if is_valid_customer(customer_id_input):
            st.session_state["customer_id"] = customer_id_input
            st.session_state["chat_active"] = True
            st.session_state["chat_history"] = []
            st.success(f"Welcome, Customer {customer_id_input}!")
        else:
            st.error("Invalid Customer ID. Please try again.")

# Step 2: Chat session
if st.session_state["chat_active"]:
    user_input = st.text_input("Ask about your order (type 'exit' to end)")
    if st.button("Submit") and user_input:
        if user_input.lower().strip() == "exit":
            st.info("🔚 Session ended. Please enter your Customer ID to start again.")
            st.session_state["customer_id"] = None
            st.session_state["chat_active"] = False
            st.session_state["chat_history"] = []
        else:
            raw = order_query_tool_func(st.session_state["customer_id"], user_input)
            final = answer_tool_func(raw)
            st.session_state["chat_history"].append((user_input, final))

    # Display chat history
    for query, response in st.session_state["chat_history"]:
        st.markdown(f"**You:** {query}")
        st.markdown(f"**Bot:** {response}")
