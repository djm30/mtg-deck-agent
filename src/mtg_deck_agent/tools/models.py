from decimal import Decimal

from pydantic import BaseModel

from mtg_deck_agent.scryfall.models import Card


class CardSummary(BaseModel):
    name: str
    mana_cost: str
    type_line: str
    oracle_text: str
    color_identity: list[str]
    price_usd: Decimal | None

    @classmethod
    def from_card(cls, card: Card) -> "CardSummary":
        return cls(
            name=card.name,
            mana_cost=card.mana_cost or "",
            type_line=card.type_line or "",
            oracle_text=card.full_oracle_text,
            color_identity=card.color_identity,
            price_usd=card.prices.usd,
        )

    def to_prompt_text(self) -> str:
        price = f"${self.price_usd}" if self.price_usd is not None else "no price"
        header = f"{self.name} | {self.mana_cost} | {self.type_line} | {price}"

        return f"{header}\n{self.oracle_text}"
