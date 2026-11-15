import random
import time
from email.utils import parsedate_to_datetime

import httpx


def retry_after_seconds(response: httpx.Response) -> float | None:
    value = response.headers.get("Retry-After")

    if value is None:
        return None

    try:
        return max(0.0, float(value))
    except ValueError:
        pass

    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None

    return max(0.0, retry_at.timestamp() - time.time())


def full_jitter_backoff(attempt: int, cap_s: float = 30.0) -> float:
    return random.uniform(0, min(cap_s, 2**attempt))
