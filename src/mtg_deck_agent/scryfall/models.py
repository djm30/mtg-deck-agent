from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScryfallModel(BaseModel):
    # Immutable; unknown fields from Scryfall are ignored (Pydantic's default)
    model_config = ConfigDict(frozen=True)


class SearchCardRequest(ScryfallModel):
    q: str
    order: str | None = None
    page: int | None = None


class Prices(ScryfallModel):
    # Scryfall sends prices as strings like "1.23", or null. There's no GBP.
    usd: Decimal | None = None
    usd_foil: Decimal | None = None
    eur: Decimal | None = None
    eur_foil: Decimal | None = None


class CardFace(ScryfallModel):
    name: str
    mana_cost: str = ""
    type_line: str | None = None
    oracle_text: str | None = None


class Card(ScryfallModel):
    id: UUID
    name: str

    # Missing on double-faced cards: those fields live in card_faces instead
    mana_cost: str | None = None
    oracle_text: str | None = None
    type_line: str | None = None
    cmc: float | None = None

    color_identity: list[str]
    legalities: dict[str, str]
    prices: Prices
    card_faces: list[CardFace] | None = None

    @property
    def is_commander_legal(self) -> bool:
        return self.legalities.get("commander") == "legal"

    @property
    def full_oracle_text(self) -> str:
        """Oracle text for single-faced cards, or every face joined for DFCs."""
        if self.oracle_text is not None:
            return self.oracle_text

        faces = self.card_faces or []
        face_texts = [face.oracle_text or "" for face in faces]

        return "\n//\n".join(face_texts)


class SearchCardResponse(ScryfallModel):
    total_cards: int
    has_more: bool
    next_page: str | None = None
    data: list[Card]
    warnings: list[str] | None = None
