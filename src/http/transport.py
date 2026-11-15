from http.rate_limit_transport import RateLimitTransport
from http.retry_transport import RetryTransport
from http.token_bucket import TokenBucket

import httpx


def build_transport(
    *,
    rate_per_s: float = 2,
    capacity: float = 1,
    max_wait_s: float = 10.0,
    max_retries: int = 3,
    inner: httpx.AsyncBaseTransport | None = None,
) -> httpx.AsyncBaseTransport:
    bucket = TokenBucket(
        capacity=capacity,
        rate_per_s=rate_per_s,
        max_wait_s=max_wait_s,
    )

    return RetryTransport(
        RateLimitTransport(inner or httpx.AsyncBaseTransport(), bucket),
        max_retries=max_retries,
        max_wait_s=max_wait_s,
    )
