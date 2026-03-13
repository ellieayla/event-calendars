from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
from scrapy.http import HtmlResponse, TextResponse

from event_calendars.items import Event
from event_calendars.spiders.burlington_green import BurlingtonGreen

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"

TODAY = datetime.now()
CUR_YEAR = TODAY.year
EASTERN = ZoneInfo("America/Toronto")



@pytest.mark.datafiles(FIXTURE_DIR / "burlington-green-events.json")
def test_parse_events_json_list(datafiles: Path) -> None:
    assert datafiles.is_dir()

    json_text: bytes = (datafiles / "burlington-green-events.json").read_bytes()

    spider = BurlingtonGreen()

    response = TextResponse(url=spider.start_urls[0], status=200, body=json_text)

    results = list(spider.parse(response))

    assert len(results) == 10

    assert results[0].url == "https://www.burlingtongreen.org/events/an-inspiring-evening-with-david-suzuki-tara-cullis/"


@pytest.mark.datafiles(FIXTURE_DIR / "burlington-green-event-30298.html")
def test_parse_event_html(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html_text: bytes = (datafiles / "burlington-green-event-30298.html").read_bytes()

    spider = BurlingtonGreen()

    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html_text)

    e: Event = spider.parse_event_details_html(response)

    assert isinstance(e, Event)
    assert e.summary == "An Inspiring Evening with David Suzuki & Tara Cullis!"
    assert e.start_datetime == datetime(2026, 3, 8, 0, 0, 0, tzinfo=ZoneInfo("America/Toronto"))
