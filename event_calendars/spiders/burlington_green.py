import logging
import warnings
from collections.abc import Iterator
from datetime import datetime, time, timedelta
from typing import Required, TypedDict
from zoneinfo import ZoneInfo

import scrapy
from scrapy.exceptions import DropItem
from scrapy.http import HtmlResponse, Response, TextResponse

from event_calendars.text_content import extract_dates_from_description, extract_dates_from_metadata, readable_text_content

from ..items import Event

BURLINGTON_TIMEZONE = ZoneInfo("America/Toronto")
DEFAULT_DURATION = timedelta(hours=2)


class WP_V2_Post(TypedDict, total=False):
    # wordpress wp-json/v2 resource
    id: Required[str]
    link: Required[str]


type WP_V2_List = list[WP_V2_Post]


class BurlingtonGreen(scrapy.Spider):
    name = "burlington-green"
    calendar_name = "Burlington Green"

    allowed_domains = ["www.burlingtongreen.org"]
    start_urls = ["https://www.burlingtongreen.org/wp-json/wp/v2/events"]

    def parse(self, response: Response) -> Iterator[scrapy.Request]:
        assert isinstance(response, TextResponse)  # guard because signature of parse() doesn't declare `response`

        posts: WP_V2_List = response.json()

        for post in posts:
            # wp_json_post_url = post["_links"]["self"][0]["href"]
            wp_html_post_url = post["link"]
            yield scrapy.Request(
                wp_html_post_url,
                callback=self.parse_event_details_html,
            )

    def parse_html_events_list(self, response: Response) -> Iterator[scrapy.Request]:
        warnings.warn(f"Use {self.parse} instead.")
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        for e in response.css("div.elementor div a::attr(href)").getall():
            yield scrapy.Request(
                response.urljoin(e),
                callback=self.parse_event_details_html,
            )

    def parse_event_details_html(self, response: Response) -> Event:
        """
        Read details from one event, and produce an Event.
        https://www.burlingtongreen.org/events/get-ready-for-community-clean-up/
        """
        assert isinstance(response, TextResponse)  # guard because signature of parse() doesn't declare `response`

        logger = logging.getLogger(self.name).getChild(response.url)

        # summary
        summary = response.css("article article h2::text").get(response.css("title::text").get())
        if not summary:
            raise DropItem("Unable to locate summary/title")

        start_datetime: datetime | None = None
        end_datetime: datetime | None = None

        # get the body content
        description = readable_text_content(response.css("article article div.elementor-widget-theme-post-content")[0].root)
        # start/end date
        header_metadata_items = response.css("article article section div.elementor-container .jet-listing-dynamic-field__content::text")

        location: str | None = None

        try:
            start_datetime, end_datetime = extract_dates_from_description(description, BURLINGTON_TIMEZONE)
            logger.info(f"Extracted {start_datetime=} {end_datetime=} from description")
        except ValueError as e:
            logger.warning(e)

        try:
            start_datetime, end_datetime = extract_dates_from_metadata([item.get() for item in header_metadata_items], BURLINGTON_TIMEZONE)
            logger.info(f"Extracted {start_datetime=} {end_datetime=} from metadata")
        except ValueError as e:
            logger.warning(e)

        if start_datetime is None:
            raise DropItem("Could not find start date in event body.")

        all_day = False
        if start_datetime.time() == time(0, 0, tzinfo=BURLINGTON_TIMEZONE):
            logger.warning("Starts at midnight")
            all_day = True

        # print(f"{all_day=}")
        if end_datetime is None:
            if all_day:
                end_datetime = start_datetime + timedelta(days=1)
            else:
                end_datetime = start_datetime + DEFAULT_DURATION

        # print(f"{response.url=} {start_datetime=} - {end_datetime=}")

        if start_datetime.tzinfo is None:
            raise ValueError(f"Did not attach timezone for {start_datetime=}", response.url)
        if end_datetime.tzinfo is None:
            raise ValueError(f"Did not attach timezone for {end_datetime=}", response.url)

        ev = Event(
            summary=summary,
            url=response.url,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            location=location,
            original_description=description,
        )
        # print(f"{ev=} has {location=}")
        return ev
