from pathlib import Path

import pytest
from scrapy.http import TextResponse

from event_calendars.items import BookableEvent
from event_calendars.spiders.burlington_hamilton_ymca import YmcaHamiltonBurlingtonPools

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "ymca-event-data-page-2026-03-14.json")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    json_text: bytes = (datafiles / "ymca-event-data-page-2026-03-14.json").read_bytes()
    assert json_text.startswith(b'[{')

    spider = YmcaHamiltonBurlingtonPools()

    response = TextResponse(
        url = '',
        status=200,
        body = json_text
    )

    results = list(spider.parse_json_classlist(response))

    from pprint import pprint
    pprint(results)

    assert len(results) == 22

    assert isinstance(results[0], BookableEvent)
