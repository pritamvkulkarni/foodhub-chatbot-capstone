import re
from agents.llm_models import llm_high_model_3

# Answer Tool: Refines raw response into customer-friendly message
def answer_tool_func(raw_response: str) -> str:
    prompt = (
        "You are a polite FoodHub customer support assistant.\n"
        "Rewrite the following raw order information into one concise, natural sentence.\n"
        "Respond directly with the final message — no labels, no explanations.\n"
        "Use friendly, professional tone suitable for a customer chat.\n"
        "If data indicates an issue or delay, express empathy briefly.\n"
        "If status is normal, keep the tone positive and reassuring.\n\n"
        "Raw data:\n"
        f"{raw_response}"
    )
    return llm_high_model_3.invoke(prompt).content

answer_tool = Tool(
    name="AnswerTool",
    func=answer_tool_func,
    description="Refines raw order data into a customer-friendly response"
)

# === Chat Agent Initialization ===

tools = [order_query_tool, answer_tool]

chat_agent = initialize_agent(
    tools=tools,
    llm=llm_high_model_3,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# === Chatbot Loop with Session ===

def chatagent():
    print("\nWelcome to OrderBot! Let's get started.")
    customer_id = input("Please enter your Customer ID: ").strip()

    if not is_valid_customer(customer_id):
        print(f"Given customer id is invalid. Please check and try again.")
        return

    print(f"\nSession started for Customer ID: {customer_id}. Type 'exit' to end the chat.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            farewell_prompt = (
                "The user is ending the chat session. Please respond with a warm, polite farewell message "
                "that thanks them for using the service and invites them to return if they need help again."
            )
            farewell_response = llm_high_model_3.invoke(farewell_prompt).content
            print(f"Bot: {farewell_response}")
            break

        try:
            # Step 1: Query order details using SQL Agent
            raw_response = order_query_tool_func(customer_id,user_input)

            # Step 2: Refine response using Answer Tool
            final_response = answer_tool_func(raw_response)

            print(f"Bot: {final_response}")
        except Exception as e:
            print(f"Error: {e}")

# === Run the Chatbot ===

if __name__ == "__main__":
    chatagent()
