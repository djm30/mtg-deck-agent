import asyncio

from langchain.agents import create_agent

from mtg_deck_agent.llm import llm
from mtg_deck_agent.tools.scryfall import search_cards

SYSTEM_PROMPT = """
You are a Magic: The Gathering assistant, focused on Commander. Answer rules
questions and help players find cards and improve their decks.

Use the search_cards tool for card text, legality and prices rather than
relying on memory, as cards get errata and new ones release often. Keep
answers short and practical, and say so when a rules question is unclear
or you're unsure.
"""

mtg_agent = create_agent(llm, system_prompt=SYSTEM_PROMPT, tools=[search_cards])


async def main() -> None:

    result = await mtg_agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Find me 5 green ramp creatures with mana value 3 or less",
                }
            ]
        }
    )

    print(result["messages"][-1].text)


if __name__ == "__main__":
    asyncio.run(main())
