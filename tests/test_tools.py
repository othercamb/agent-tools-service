import pytest

pytestmark = pytest.mark.skip(reason="Day 4: delete this line when you start")


def test_existing_order(client):
    response = client.get("/tools/order-status/ORD-1001")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_transit"
    assert body["eta"] == "2026-09-24"


def test_unknown_order_returns_404(client):
    response = client.get("/tools/order-status/ORD-9999")
    assert response.status_code == 404


def test_malformed_id_is_rejected(client):
    response = client.get("/tools/order-status/DROP-TABLE")
    assert response.status_code in (404, 422)
