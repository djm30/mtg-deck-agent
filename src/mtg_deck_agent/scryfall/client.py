from typing import Any, Self

import httpx

from mtg_deck_agent.scryfall.models import SearchCardResponse
from mtg_deck_agent.scryfall.routes import SLOW_ROUTES, Route
from mtg_deck_agent.transport.errors import ApiError
from mtg_deck_agent.transport.rate_limit_transport import RateLimitTransport
from mtg_deck_agent.transport.retry_transport import RetryTransport
from mtg_deck_agent.transport.token_bucket import TokenBucket

BASE_URL = "https://api.scryfall.com"

# Scryfall requires a descriptive User-Agent and an Accept header
HEADERS = {
    "User-Agent": "MtgDeckAgent/0.1",
    "Accept": "application/json",
}


class ScryfallError(ApiError):
    """An error response from Scryfall, with its error code and details."""

    def __init__(self, status_code: int, code: str, details: str) -> None:
        super().__init__(f"{status_code} {code}: {details}", status_code=status_code)
        self.code = code
        self.details = details


def build_scryfall_transport(
    *,
    max_retries: int = 3,
    inner: httpx.AsyncBaseTransport | None = None,
) -> httpx.AsyncBaseTransport:

    slow_bucket = TokenBucket(rate_per_s=2, capacity=1)

    default_bucket = TokenBucket(
        capacity=1,
        rate_per_s=10.0,
    )

    rate_limit_transport = RateLimitTransport(
        inner or httpx.AsyncHTTPTransport(),
        bucket=default_bucket,
        buckets_by_prefix={route: slow_bucket for route in SLOW_ROUTES},
    )

    return RetryTransport(
        inner=rate_limit_transport,
        max_retries=max_retries,
    )


class ScryfallClient:
    """Create once and reuse, so every call shares the same rate limits."""

    def __init__(
        self,
        *,
        timeout_s: float = 10.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._http = httpx.AsyncClient(
            base_url=BASE_URL,
            headers=HEADERS,
            timeout=timeout_s,
            transport=transport or build_scryfall_transport(),
        )

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def search_cards(self, query: str) -> SearchCardResponse:
        """Raises ScryfallError with code "not_found" when nothing matches."""
        response = await self._get(Route.SEARCH, params={"q": query})

        return SearchCardResponse.model_validate_json(response.content)

    async def _get(self, path: str, **kwargs: Any) -> httpx.Response:
        response = await self._http.get(path, **kwargs)

        if response.is_error:
            raise _scryfall_error(response)

        return response


def _scryfall_error(response: httpx.Response) -> ScryfallError:
    """Build an error from Scryfall's JSON error body, if it sent one."""
    try:
        body = response.json()
    except ValueError:
        body = {}

    return ScryfallError(
        status_code=response.status_code,
        code=body.get("code", "unknown"),
        details=body.get("details", response.text),
    )
