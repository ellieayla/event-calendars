import pytest

from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

from scrapy.http import HtmlResponse

from ..items import Event
from event_calendars.spiders.respect_cyclists import RespectCyclistsFacebookEvents


FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "facebook-respectcyclists-events-list.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "facebook-respectcyclists-events-list.html").read_bytes()
    assert html.startswith(b'<html id="facebook"')

    spider = RespectCyclistsFacebookEvents()

    response = HtmlResponse(
        url = 'https://www.facebook.com/groups/respectcyclists/events',
        status=200,
        body = html
    )

    results = spider.parse(response)

    urls = [result.url for result in results]
    assert urls == [
        'https://www.facebook.com/events/789092220770764/',
        'https://www.facebook.com/events/2533827373664092/',
        'https://www.facebook.com/events/783985534010634/',
    ]


@pytest.mark.datafiles(FIXTURE_DIR / "facebook-events-789092220770764.html")
def test_parse_single_event_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "facebook-events-789092220770764.html").read_bytes()

    assert html.startswith(b'<html id="facebook"')
    assert b'789092220770764' in html
    assert b'start_timestamp' in html

    spider = RespectCyclistsFacebookEvents()

    response = HtmlResponse(
        url = 'https://www.facebook.com/events/789092220770764/',
        status=200,
        body = html
    )

    result = list(spider.parse_single_event_page(response))

    assert len(result) == 1
    event = result[0]

    assert isinstance(event, Event)
    assert event.summary == "Ghost Bike Ride For Jean Louis"

    ref_date = datetime(2025, 11, 1, 14, 0, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert ref_date.tzinfo == ZoneInfo('America/Toronto')

    assert event.start_datetime == datetime(2025, 11, 1, 14, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert event.url == response.url
    assert 'Harvester' in event.description
