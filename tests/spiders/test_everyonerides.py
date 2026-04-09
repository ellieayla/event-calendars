from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from scrapy import Request
from scrapy.http import HtmlResponse

from event_calendars.items import Event
from event_calendars.spiders.everyonerides import EveryoneRides

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "everyonerides-org-events.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "everyonerides-org-events.html").read_bytes()

    spider = EveryoneRides()
    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html)

    results = list(spider.parse(response))
    assert isinstance(results[0], Request)

    assert results[0].url == "https://www.everyonerides.org/bike_share_birthday_party"


@pytest.mark.datafiles(FIXTURE_DIR / "everyonerides-org-bike_share_birthday_party.html")
def test_parse_single_event_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "everyonerides-org-bike_share_birthday_party.html").read_bytes()

    spider = EveryoneRides()
    response = HtmlResponse(url="https://www.everyonerides.org/bike_share_birthday_party", status=200, body=html)

    event: Event = spider.parse_details_page(response)

    assert event.summary == "Bike Share Birthday Party"

    assert event.start_datetime == datetime(2026, 3, 20, 18, 30, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert event.url == response.url
    assert "Sterling & Forsyth" in event.description
