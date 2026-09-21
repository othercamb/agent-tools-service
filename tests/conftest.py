import pytest
from fastapi.testclient import TestClient

from tools_service.config import get_settings
from tools_service.main import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    """A fresh app with its own temporary database for every test."""
    monkeypatch.setenv("DATABASE_PATH", str(tmp_path / "test.db"))
    monkeypatch.setenv("WEBHOOK_SECRET", "test-secret")
    get_settings.cache_clear()
    with TestClient(create_app()) as c:
        yield c
    get_settings.cache_clear()
