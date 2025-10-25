
HIGH_TEMP = 1.0 # High Temperature
LOW_TEMP  = 0.0 # Low  Temperature

#TODO: remove hardcoding
groq_api_key = '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'

# High creativity LLM
llm_high_model_3 = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=HIGH_TEMP,
    groq_api_key=groq_api_key)

# Low creativity (deterministic) LLM
llm_model_3 = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=LOW_TEMP,
    groq_api_key=groq_api_key
)
