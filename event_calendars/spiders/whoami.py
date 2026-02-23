import scrapy
from scrapy.http import HtmlResponse, TextResponse, Response
from typing import Iterator, Any

from ..items import Event

import icalendar
import logging
from datetime import datetime, timedelta

from html2text import html2text

from .registry import register


@register
class WhoamiSpider(scrapy.Spider):
    name = 'whoami'
    allowed_domains = ['whoami.labs.verselogic.net']
    start_urls = [
        'http://whoami.labs.verselogic.net'
    ]

    def parse(self, response: Response) -> Iterator[Event]:
        assert isinstance(response, TextResponse)  # guard because signature of parse() doesn't declare `response`

        _fake_date = datetime.fromisoformat("2020-01-01T13:30:00Z")  # needed by exporter but unimportant

        e = Event(
            summary = "whoami-event",
            url = response.url,

            start_datetime = _fake_date,
            end_datetime = _fake_date + timedelta(hours=1),

            location = "whoami",
            original_description = response.text,
        )
        print(f"{e=}")
        yield e
