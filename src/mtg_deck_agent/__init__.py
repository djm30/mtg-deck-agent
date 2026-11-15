from langchain.agents import create_agent
from langchain_core.tools import tool

from main import llm

SYSTEM_PROMPT = """
You are a Magic the Gathering assistant agent, answer questions on rules,
and give helpful suggestions to players
"""

mtg_agent = create_agent(llm, system_prompt=SYSTEM_PROMPT)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
