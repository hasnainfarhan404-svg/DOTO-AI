import os
import asyncio
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled

# Disable tracing to avoid platform.openai.com API key errors when using custom providers
set_tracing_disabled(True)

# Load environment variables from .env
load_dotenv(find_dotenv())

# Page Configuration
st.set_page_config(page_title="AI Agent Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 AI Agent Chatbot")
st.caption("Powered by OpenAI Agents SDK & OpenRouter")

# Initialize External OpenAI Client (OpenRouter)
external_client = AsyncOpenAI(
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# Initialize Model
llm_model = OpenAIChatCompletionsModel(
    model="inclusionai/ling-3.0-flash:free",
    openai_client=external_client
)

# Initialize Agent (Instructions updated for name DOTO AI)
agent = Agent(
    name="DOTO AI",
    instructions="Your name is DOTO AI. Always introduce yourself as DOTO AI when asked about your name or who you are. You are a helpful, friendly, and concise AI assistant.",
    model=llm_model
)

# Initialize Chat History in Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Type your message here..."):
    # Render user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using OpenAI Agents SDK
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Synchronous execution of the agent run
                result = Runner.run_sync(
                    starting_agent=agent,
                    input=prompt
                )
                response_text = result.final_output
                st.markdown(response_text)
                
                # Save assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Error generating response: {e}")
