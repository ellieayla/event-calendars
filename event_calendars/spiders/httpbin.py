from collections.abc import Iterator
from datetime import datetime, timedelta

import scrapy
from scrapy.http import Response, TextResponse

from ..items import Event


class HttpBinSpider(scrapy.Spider):
    name = 'httpbin'
    skip_in_runall = True

    allowed_domains = ['httpbin.org']
    start_urls = [
        'https://httpbin.org/json'
    ]

    def parse(self, response: Response) -> Iterator[Event]:
        assert isinstance(response, TextResponse)

        _fake_date = datetime.fromisoformat("2020-01-01T13:30:00Z")  # needed by exporter but unimportant

        e = Event(
            summary = "httpbin-event",
            url = response.url,

            start_datetime = _fake_date,
            end_datetime = _fake_date + timedelta(hours=1),

            updated_at = _fake_date,

            location = "whoami",
            original_description = response.text,
        )
        print(f"{e=}")
        yield e
