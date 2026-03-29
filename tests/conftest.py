import pytest


@pytest.fixture(autouse=True)
def no_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    """Remove requests.sessions.Session.request for all tests."""
    monkeypatch.delattr("requests.sessions.Session.request")
    monkeypatch.delattr("scrapy.core.downloader.Downloader.fetch")
    monkeypatch.delattr("urllib.request")
