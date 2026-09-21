import hashlib
import hmac
import json

import pytest

pytestmark = pytest.mark.skip(reason="Day 5: delete this line when you start")

SECRET = "test-secret"
EVENT = {
    "event_id": "evt-1",
    "conversation_id": "conv-1",
    "summary": "Customer asked about ORD-1001",
    "data": {"order_id": "ORD-1001"},
}


def sign(body: bytes) -> str:
    return "sha256=" + hmac.new(SECRET.encode(), body, hashlib.sha256).hexdigest()


def post(client, body: bytes, signature: str | None):
    headers = {"Content-Type": "application/json"}
    if signature is not None:
        headers["X-Signature"] = signature
    return client.post("/webhooks/post-call", content=body, headers=headers)


def test_valid_signature_is_accepted(client):
    body = json.dumps(EVENT).encode()
    response = post(client, body, sign(body))
    assert response.status_code == 200
    assert response.json() == {"accepted": True}


def test_bad_signature_is_rejected(client):
    body = json.dumps(EVENT).encode()
    assert post(client, body, "sha256=deadbeef").status_code == 401


def test_missing_signature_is_rejected(client):
    body = json.dumps(EVENT).encode()
    assert post(client, body, None).status_code == 401


def test_duplicate_event_is_idempotent(client):
    body = json.dumps(EVENT).encode()
    first = post(client, body, sign(body))
    second = post(client, body, sign(body))
    assert first.json() == {"accepted": True}
    assert second.json() == {"duplicate": True}
