from http.transport import build_transport

import httpx

BASE_URL = "https://api.scryfall.com"
HEADERS = {
    "User-Agent": "mtg-deck-agent/0.1 (personal learning project)",
    "Accept": "application/json",
}
MIN_INTERVAL_S = 0.5


class ScryfallError(Exception):
    """Scryfall returned something unexpected"""


class ScryfallClient:
    def __init__(self, timeout: float = 10.0) -> None:

        transport = build_transport(rate_per_s=2, capacity=2)

        self._http = httpx.Client(
            base_url=BASE_URL, headers=HEADERS, timeout=timeout, transport=transport
        )

    async def search_cards(self):
        return self._http.get()
