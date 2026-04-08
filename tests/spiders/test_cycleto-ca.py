from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from scrapy import Request
from scrapy.http import HtmlResponse

from event_calendars.items import Event
from event_calendars.spiders.cycleto import CycleToronto

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "cycleto-ca-events.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "cycleto-ca-events.html").read_bytes()

    spider = CycleToronto()
    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html)

    results = list(spider.parse(response))
    assert isinstance(results[0], Request)

    assert results[0].url == "https://www.cycleto.ca/public_meeting_high_park_movement_strategy"


@pytest.mark.datafiles(FIXTURE_DIR / "cycleto.ca-event-cdoyr-2026.html")
def test_parse_single_event_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "cycleto.ca-event-cdoyr-2026.html").read_bytes()

    spider = CycleToronto()
    response = HtmlResponse(url="https://www.cycleto.ca/cdoyr_2026", status=200, body=html)

    event: Event = spider.parse_details_page(response)

    assert event.summary == "Coldest Day of the Year Ride 2026"

    # event starts at 10am Eastern, aka 1500h UTC
    ref_date = datetime(2026, 2, 28, 10, 0, 0, tzinfo=ZoneInfo('America/Toronto'))
    assert ref_date.tzinfo == ZoneInfo('America/Toronto')

    assert event.start_datetime == ref_date
    assert event.url == response.url
    assert "Sugar Beach Park" in event.description
    # note, rest of description formatting in module test_readable_text_content
