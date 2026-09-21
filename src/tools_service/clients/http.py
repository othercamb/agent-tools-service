import httpx


class ResilientClient:
    """Day 3: an async HTTP client with timeouts and retries with exponential backoff.

    Requirements (tests/test_http_client.py checks these):
      - retry on network errors and on HTTP 429 / 5xx
      - do NOT retry on other 4xx (a bad request will not fix itself)
      - wait base_delay * 2**attempt between attempts
      - give up after max_attempts and raise the last error
    """

    def __init__(
        self,
        client: httpx.AsyncClient,
        max_attempts: int = 3,
        base_delay: float = 0.2,
    ) -> None:
        self.client = client
        self.max_attempts = max_attempts
        self.base_delay = base_delay

    async def get_json(self, url: str) -> dict:
        raise NotImplementedError("Day 3")
