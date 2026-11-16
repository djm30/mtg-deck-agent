import asyncio
import time
from collections.abc import Awaitable, Callable

from mtg_deck_agent.transport.errors import RateLimitError

Clock = Callable[[], float]
Sleep = Callable[[float], Awaitable[None]]

TOKEN_TOLERANCE = 1e-9


class TokenBucket:
    def __init__(
        self,
        capacity: float,
        rate_per_s: float,
        *,
        max_wait_s: float = 10.0,
        clock: Clock = time.monotonic,
        sleep: Sleep = asyncio.sleep,
    ):
        self._capacity = capacity
        self._tokens = capacity
        self._rate_per_s = rate_per_s
        self._last_refill_ts = 0
        self._max_wait_s = max_wait_s

        self._clock = clock
        self._sleep = sleep

        self._cooldown_until_ts = self._clock()

        # Requests take the lock, requests attempting to take a locked lock are queued
        self._queue = asyncio.Lock()

    async def _wait_for_token(self, cost: float, deadline_ts: float):
        while True:
            now_ts = self._clock()

            self.refill()

            # We have the capacity, request can proceed
            if self._tokens >= cost:
                self._tokens = self._tokens - cost
                return

            # How many tokens do we need, and how long will it take to earn them
            tokens_needed = cost - self._tokens

            cooldown_left_s = max(0.0, self._cooldown_until_ts - now_ts)
            time_needed_s = cooldown_left_s + (tokens_needed / self._rate_per_s)
            ready_at = now_ts + time_needed_s

            if ready_at > deadline_ts:
                raise RateLimitError(retry_after_s=time_needed_s)

            await self._sleep(time_needed_s)

    async def take(self, cost: float = 1):
        now_ts = self._clock()
        deadline_ts = now_ts + self._max_wait_s

        if cost > self._capacity:
            raise ValueError("Cost exceeds given capacity for this bucket")

        async with self._queue:
            return await self._wait_for_token(cost, deadline_ts)

    def cooldown_for(self, seconds: float):
        now_ts = self._clock()

        self._tokens = 0
        # Don't overwrite existing cooldown if incoming is shorter
        self._cooldown_until_ts = max(self._cooldown_until_ts, now_ts + seconds)

    def refill(self):
        now_ts = self._clock()

        # Refill window starts from either last refill, or the end ts of the last cooldown
        refill_start_ts = max(self._last_refill_ts, self._cooldown_until_ts)
        elapsed_s = now_ts - refill_start_ts

        if elapsed_s > 0:
            tokens_earned = elapsed_s * self._rate_per_s
            refilled_amount = self._tokens + tokens_earned
            self._tokens = min(self._capacity, refilled_amount)

        self._last_refill_ts = now_ts
