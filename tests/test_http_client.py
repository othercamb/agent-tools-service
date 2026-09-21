import httpx
import pytest

from tools_service.clients.http import ResilientClient

pytestmark = pytest.mark.skip(reason="Day 3: delete this line when you start")


def make_http(responses):
    """Fake transport: returns (or raises) the given items in order."""
    calls = {"n": 0}

    def handler(request):
        item = responses[min(calls["n"], len(responses) - 1)]
        calls["n"] += 1
        if isinstance(item, Exception):
            raise item
        return item

    return httpx.AsyncClient(transport=httpx.MockTransport(handler)), calls


async def test_retries_on_5xx_then_succeeds():
    http, calls = make_http(
        [httpx.Response(503), httpx.Response(503), httpx.Response(200, json={"ok": True})]
    )
    client = ResilientClient(http, max_attempts=3, base_delay=0)
    assert await client.get_json("https://api.test/orders") == {"ok": True}
    assert calls["n"] == 3


async def test_retries_on_429():
    http, calls = make_http([httpx.Response(429), httpx.Response(200, json={"ok": True})])
    client = ResilientClient(http, max_attempts=3, base_delay=0)
    assert await client.get_json("https://api.test/orders") == {"ok": True}
    assert calls["n"] == 2


async def test_does_not_retry_on_400():
    http, calls = make_http([httpx.Response(400)])
    client = ResilientClient(http, max_attempts=3, base_delay=0)
    with pytest.raises(httpx.HTTPStatusError):
        await client.get_json("https://api.test/orders")
    assert calls["n"] == 1


async def test_gives_up_after_max_attempts_on_network_error():
    http, calls = make_http([httpx.ConnectError("connection refused")])
    client = ResilientClient(http, max_attempts=3, base_delay=0)
    with pytest.raises(httpx.ConnectError):
        await client.get_json("https://api.test/orders")
    assert calls["n"] == 3
