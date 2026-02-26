from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from scrapy.http import HtmlResponse

from event_calendars.items import Event
from event_calendars.spiders.newhope import TourDeCafe

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "newhope-tourdecafe.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "newhope-tourdecafe.html").read_bytes()
    assert b"Squarespace" in html

    spider = TourDeCafe()
    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html)

    result = list(spider.parse(response))

    assert len(result) == 12
    event = result[0]

    assert isinstance(event, Event)
    assert event.summary == "Tour de Cafe - May 10"

    assert event.start_datetime == datetime(2025, 5, 10, 8, 0, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert event.url == response.url
    assert 'novice' in event.description
