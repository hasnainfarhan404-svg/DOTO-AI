from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

external_client = AsyncOpenAI(
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

llm_model = OpenAIChatCompletionsModel(
    model="inclusionai/ling-3.0-flash:free",
    openai_client=external_client,
)

agent = Agent(
    name="Personal Assistant",
    instructions="help me with my tasks and answer my questions.",
    model=llm_model,
)

result = Runner.run_sync(
    starting_agent=agent,
    input="",
)

print(result.final_output)