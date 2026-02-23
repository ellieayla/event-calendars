import scrapy
from scrapy.http import TextResponse, Response
from typing import Iterator

from ..items import Event

from datetime import datetime, timedelta


class MergeSpider(scrapy.Spider):
    name = 'merge'
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
