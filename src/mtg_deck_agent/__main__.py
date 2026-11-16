import asyncio

from mtg_deck_agent.agent import mtg_agent


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
