from datetime import datetime

from scrapy.http import TextResponse

from event_calendars.items import Event
from event_calendars.spiders.httpbin import HttpBinSpider


def test_httpbin_stub() -> None:
    s = HttpBinSpider()

    response = TextResponse(
        url=s.start_urls[0],
        status=200,
        body=b"whatever"
    )
    e: Event = next(s.parse(response=response))

    assert isinstance(e.start_datetime, datetime)
    assert e.summary == "httpbin-event"
