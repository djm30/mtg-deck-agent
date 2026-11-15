from langchain_openai import ChatOpenAI

from mtg_deck_agent.env import Environment

env = Environment()

llm = ChatOpenAI(api_key=env.OPENAI_API_KEY, model=env.MODEL, base_url=env.OPEN_AI_BAASE_URL)
