import logging
from collections.abc import Iterator
from typing import Any

import icalendar
import scrapy
from html2text import html2text
from scrapy.http import HtmlResponse, Response, TextResponse

from ..items import Event


class TorontoCommunityBikeways(scrapy.Spider):
    name = "toronto-community-bikeways"
    calendar_name = "Toronto Community Bikeways"

    allowed_domains = ["www.communitybikewaysto.ca"]
    start_urls = ["https://www.communitybikewaysto.ca/events"]

    def parse(self, response: Response) -> Iterator[scrapy.Request]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        for e in response.css("div.events-list .eventlist-event h1 a::attr(href)").getall():
            yield scrapy.Request(
                response.urljoin(e),
                callback=self.parse_meeting_details,
            )

    def parse_meeting_details(self, /, *args: Any, **kwargs: Any) -> Iterator[scrapy.Request]:
        assert isinstance(args[0], HtmlResponse)  # guard because signature of parse() doesn't declare `response`
        response: HtmlResponse = args[0]

        # one event, like /events/roqzijbovnaaa6t243n3f1xggq8mkk
        ics_url: str = response.css("a.eventitem-meta-export-ical::attr(href)").get() or ""

        content = response.css(".events-item .html-block")

        try:
            description = html2text(content.get() or "")
        except AttributeError:
            description = ""

        yield scrapy.Request(
            response.urljoin(ics_url),
            callback=self.handle_ical_file,
            cb_kwargs={
                "event_url": response.url,
                "description": description,
            },
        )

    def handle_ical_file(self, response: Response, event_url: str, description: str) -> Iterator[Event]:
        assert isinstance(response, TextResponse)  # guard because signature of parse() doesn't declare `response`

        base_calendar: icalendar.Calendar = icalendar.Calendar.from_ical(response.text, multiple=False)

        base_event = base_calendar.events[0]

        location = base_event.decoded("location", default="")
        start_time = base_event.decoded("dtstart")
        end_time = base_event.decoded("dtend")
        dtstamp_updated_at_datetime = base_event.decoded("dtstamp")
        url = base_event.decoded("url", default="")
        summary = base_event.decoded("summary")

        if url and url != event_url:
            logging.warning("Url in ical file does not match page url")

        e = Event(
            summary=summary,
            url=event_url,
            start_datetime=start_time,
            end_datetime=end_time,
            updated_at=dtstamp_updated_at_datetime,
            location=location,
            original_description=description,
        )
        print(f"{e=} has {location=}")
        yield e
