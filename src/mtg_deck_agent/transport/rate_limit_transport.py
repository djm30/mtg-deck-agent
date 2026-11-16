from collections.abc import Mapping

import httpx

from mtg_deck_agent.transport.token_bucket import TokenBucket
from mtg_deck_agent.transport.utils import retry_after_seconds


class RateLimitTransport(httpx.AsyncBaseTransport):
    """Takes a token before each request, starts a cooldown on 429"""

    def __init__(
        self,
        inner: httpx.AsyncBaseTransport,
        bucket: TokenBucket,
        *,
        buckets_by_prefix: Mapping[str, TokenBucket] | None = None,
        default_cooldown_s: float = 1.0,
    ) -> None:

        self._inner = inner
        self._default_bucket = bucket
        self._default_cooldown_s = default_cooldown_s
        self._buckets_by_prefix = buckets_by_prefix

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        bucket = self._bucket_for(request)
        await bucket.take()

        response = await self._inner.handle_async_request(request)

        if response.status_code == 429:
            delay_s = retry_after_seconds(response)
            delay_s = delay_s if delay_s else self._default_cooldown_s
            bucket.cooldown_for(delay_s)

        return response

    def _bucket_for(self, request: httpx.Request) -> TokenBucket:
        if self._buckets_by_prefix is None:
            return self._default_bucket

        path = request.url.path

        for prefix, bucket in self._buckets_by_prefix.items():
            if path.startswith(prefix):
                return bucket

        return self._default_bucket

    async def aclose(self) -> None:
        await self._inner.aclose()
