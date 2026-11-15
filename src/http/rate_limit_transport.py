from http.token_bucket import TokenBucket
from http.utils import retry_after_seconds

import httpx


class RateLimitTransport(httpx.AsyncBaseTransport):
    """Takes a token before each request, starts a cooldown on 429"""

    def __init__(
        self,
        inner: httpx.AsyncBaseTransport,
        bucket: TokenBucket,
        *,
        default_cooldown_s: float = 1.0,
    ) -> None:
        super.__init__()

        self._inner = inner
        self._bucket = bucket
        self._default_cooldown_s = default_cooldown_s

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        await self._bucket.take()

        response = await self._inner.handle_async_request(request)

        if response.status_code == 429:
            delay_s = retry_after_seconds(response)
            self._bucket.cooldown_for(delay_s)

        return response

    async def aclose(self) -> None:
        await self._inner.aclose()
