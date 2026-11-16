from langchain.tools import tool

from mtg_deck_agent.scryfall.client import ScryfallClient, ScryfallError
from mtg_deck_agent.tools.models import CardSummary

scryfall = ScryfallClient()


@tool
async def search_cards(query: str) -> str:
    """Search Scryfall for Magic cards using Scryfall query syntax.

    Use this to find cards by rules text, type, colour identity, cost or price.
    Returns up to 20 cards and the total number of matches. If the total is
    much larger than 20, narrow the query rather than assuming you saw everything.
    An empty result means nothing matched, so loosen the query.

    Args:
        query: A Scryfall search query. Terms separated by spaces must all match.
            Useful terms:
            - id<=wub          fits a W/U/B commander's colour identity
            - t:creature       type line contains "creature"
            - o:"draw a card"  oracle text contains the phrase
            - mv<=3            mana value 3 or less
            - f:commander      legal in Commander
            - usd<5            costs under $5
            - otag:ramp        tagged by role, e.g. ramp, removal, card-advantage
            Example: id<=gu f:commander t:creature o:"enters the battlefield" mv<=4
    """

    try:
        results = await scryfall.search_cards(query)
    except ScryfallError as e:
        if e.code == "not_found":
            return format_search_result(query=query, total=0, cards=[])
        raise

    cards = [CardSummary.from_card(card) for card in results.data[:20]]

    return format_search_result(query=query, total=results.total_cards, cards=cards)


def format_search_result(query: str, total: int, cards: list[CardSummary]) -> str:
    if not cards:
        return f'No cards matched "{query}". Loosen the query: drop a term or widen the colour identity.'

    header = f"Found {total} cards, showing {len(cards)}."
    if total > len(cards):
        header += " Narrow the query to see more relevant results."

    card_blocks = [card.to_prompt_text() for card in cards]

    return "\n\n".join([header, *card_blocks])
