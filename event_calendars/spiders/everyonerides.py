from collections.abc import Iterator
from datetime import timedelta
from zoneinfo import ZoneInfo

import scrapy
import scrapy.http
from scrapy.exceptions import DropItem

from ..items import Event
from ..text_content import extract_dates_from_description, readable_text_content

BURLINGTON_TIMEZONE = ZoneInfo("America/Toronto")
DEFAULT_DURATION = timedelta(hours=2)


class EveryoneRides(scrapy.Spider):
    name = "everyone-rides"
    calendar_name = "Everyone Rides"

    allowed_domains = ["www.everyonerides.org"]
    start_urls = ["https://www.everyonerides.org/events"]

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        for event_url in response.css(".content-container ul.event-wrap li h3 a::attr(href)").getall():
            yield scrapy.Request(
                url=response.urljoin(event_url),
                callback=self.parse_details_page,
            )

    def parse_details_page(self, response: scrapy.http.Response) -> Event:

        summary = response.css("h2::text").get(response.css("title::text").get())
        if not summary:
            raise DropItem("No event name found in h2/title")

        description = readable_text_content(response.css("#content #intro")[0].root)

        when_block = response.css("#content .event-detail").xpath("div[contains(., 'WHEN')]/parent::div").css(".subtext::text").get()
        if when_block:
            start_time, end_time = extract_dates_from_description(when_block, BURLINGTON_TIMEZONE)
        else:
            start_time, end_time = extract_dates_from_description(description, BURLINGTON_TIMEZONE)

        if end_time is None:
            self.logger.warning(f"No end time found for {response.url}, setting 2h")
            end_time = start_time + DEFAULT_DURATION

        where_block_parent = response.css("#content .event-detail").xpath("div[contains(., 'WHERE')]/parent::div").css(".subtext")
        where_block_parent.css("a").drop()

        if where_block_parent:
            location = readable_text_content(where_block_parent[0].root).replace("\n", ", ")
        else:
            location = "See post"

        return Event(
            summary=summary,
            start_datetime=start_time,
            end_datetime=end_time,
            url=response.url,
            location=location,
            original_description=description,
        )
