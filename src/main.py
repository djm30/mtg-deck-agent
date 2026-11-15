from langchain_core.language_models.base import LanguageModelInput

from mtg_deck_agent.env import Environment
from mtg_deck_agent.llm import llm

env = Environment()

messages: LanguageModelInput = [
    ("system", "Translate any input from English into French"),
    ("user", "Hello World!"),
]

response = llm.invoke(messages)

print(response.content)


second_response = llm.invoke([*messages, ("user", "Whats up gang")])


print(second_response.content)
