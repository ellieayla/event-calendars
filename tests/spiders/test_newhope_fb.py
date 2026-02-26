from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from scrapy.http import HtmlResponse

from event_calendars.items import Event
from event_calendars.spiders.newhope import TourDeCafeFacebook

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "newhope-tourdecafe-facebook-groups-643937107228046-events.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "newhope-tourdecafe-facebook-groups-643937107228046-events.html").read_bytes()
    assert b'<html id="facebook"' in html[0:100]

    spider = TourDeCafeFacebook()
    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html)

    results = spider.parse(response)

    urls = [result.url for result in results]
    assert urls == [
        'https://www.facebook.com/events/1936571343795753/',
        'https://www.facebook.com/events/25032520543005120/',
        'https://www.facebook.com/events/712363534995252/',
    ]


@pytest.mark.datafiles(FIXTURE_DIR / "newhope-tourdecafe-facebook-1936571343795753.html")
def test_parse_single_event_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "newhope-tourdecafe-facebook-1936571343795753.html").read_bytes()

    assert b'<html id="facebook"' in html[0:100]
    assert b'1936571343795753' in html
    assert b'start_timestamp' in html

    spider = TourDeCafeFacebook()
    response = HtmlResponse(url="blah", status=200, body=html)

    result = list(spider.parse_single_event_page(response))

    assert len(result) == 1
    event = result[0]

    assert isinstance(event, Event)
    assert event.summary == "Tour de Cafe - October 18"
    assert event.start_datetime == datetime(2025, 10, 18, 8, 0, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert event.url == response.url
    assert 'novice' in event.description
