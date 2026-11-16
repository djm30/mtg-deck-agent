class ApiError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RateLimitError(ApiError):
    def __init__(self, retry_after_s: float) -> None:
        super().__init__(f"Rate limited, retry in {retry_after_s:.1f}s", status_code=429)
        self.retry_after_s = retry_after_s
