import asyncio
from collections.abc import Callable
from http.token_bucket import Sleep
from http.utils import full_jitter_backoff, retry_after_seconds

import httpx

IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})
RETRYABLE_SERVER_ERRORS = frozenset({502, 503, 504})


class RetryTransport(httpx.AsyncBaseTransport):
    """
    Retries 429 for any method, and 502/503/504 for idempotent methods

     Backoffs over max_wait_s are skipped, returning the error response as is
    """

    def __init__(
        self,
        inner: httpx.AsyncBaseTransport,
        *,
        max_retries: int = 3,
        max_wait_s: float = 10.0,
        backoff: Callable[[float], float] = full_jitter_backoff,
        sleep: Sleep = asyncio.sleep,
    ):
        self._inner = inner
        self._max_retries = max_retries
        self._max_wait_s = max_wait_s
        self._backoff = backoff
        self._sleep = sleep()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        # Initial attempt not counted towards max retries
        for attempt in range(self._max_retries + 1):
            response = await self._inner.handle_async_request(request)

            # Attempt 1 is the retry 1
            if attempt == self._max_retries or not self._should_retry(request, response):
                return response

            delay_s = retry_after_seconds(response)
            if delay_s is None:
                delay_s = self._backoff(attempt)

            if delay_s > self._max_wait_s:
                return response

            await response.aclose()
            await self._sleep(delay_s)

        return response

    @staticmethod
    def _should_retry(request: httpx.Request, response: httpx.Response) -> bool:
        if response.status_code == 429:
            return True

        return (
            response.status_code in RETRYABLE_SERVER_ERRORS and request.method in IDEMPOTENT_METHODS
        )

    async def aclose(self) -> None:
        await self._inner.aclose()
