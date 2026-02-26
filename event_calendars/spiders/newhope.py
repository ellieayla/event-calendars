import json
import re
from collections.abc import Iterator
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Request, Response
from scrapy.selector.unified import Selector

from event_calendars.utils import readable_text_content

from ..fb_graphql import Event as FBEvent
from ..fb_graphql import RelayPrefetchedStreamCache_Result, extract_prefetched_events_from_inline_json, extract_prefetched_objects_from_inline_json
from ..items import Event
from ..timezone_lookup import discover_zoneinfo_for_shortname

HAMILTON_TIMEZONE = ZoneInfo("America/Toronto")
ESTIMATED_DURATION = timedelta(hours=2)
DEFAULT_DESCRIPTION = "Tour de Cafe is a novice cycling group ride"


class TourDeCafe(scrapy.Spider):
    name = 'tour-de-cafe-newhope'
    calendar_name = "Tour de Cafe, New Hope"
    skip_in_runall = True

    allowed_domains = ["www.newhopecommunitybikes.com"]
    start_urls = ["https://www.newhopecommunitybikes.com/womens-programming"]

    def parse(self, response: Response) -> Iterator[Event]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        html_blocks = response.css(".main-content div div.row div.col.span-12 div.html-block")

        inside_tour_de_cafe_chunk = False
        tour_de_cafe_chunk = None
        description = DEFAULT_DESCRIPTION

        for block in html_blocks:
            if block.css("h1 ::text").get() == "Tour De Cafe":
                inside_tour_de_cafe_chunk = True
                description = readable_text_content(block.css("p")[0].root)
                continue

            if inside_tour_de_cafe_chunk:

                tour_de_cafe_chunk = block.css("div.sqs-html-content")[0]
                break

        if tour_de_cafe_chunk is None:
            raise CloseSpider(reason="Could not find list of dates for Tour de Cafe")

        assert isinstance(tour_de_cafe_chunk, Selector)
        published_schedule_text = readable_text_content(tour_de_cafe_chunk.root)

        for (start_datetime, extra_text) in extract_dates_from_text(published_schedule_text):
            # NOTE: Summary matches normal ones from facebook, to dedupe against.
            yield Event(
                summary=f"Tour de Cafe{" to " + extra_text if extra_text else ""} - {start_datetime.strftime("%B %-d")}",
                start_datetime=start_datetime,
                end_datetime=start_datetime+ESTIMATED_DURATION,
                url=response.url,
                location="New Hope Community Bikes, 1249 Main Street East, Hamilton Ontario",
                original_description=description,
                )


def extract_dates_from_text(published_schedule_text: str) -> Iterator[tuple[datetime, str]]:
    YEAR_PATTERN = re.compile(r"(\d{4}).*date")
    year: str|None = None

    schedule_pieces = published_schedule_text.splitlines()
    for p in schedule_pieces:
        if p == "":
            continue
        if p.startswith("* "):
            if year is None:
                raise ValueError("Did not find year before bulleted list of dates!", schedule_pieces)
            (month_day_string, _, extra_info) = p.partition("-")
            start_datetime = datetime.strptime(month_day_string.strip() + f", {year}, 08:00", "* %B %d, %Y, %H:%M").replace(tzinfo=HAMILTON_TIMEZONE)
            yield (start_datetime, extra_info.strip())
            continue
        else:
            year = None
            m = YEAR_PATTERN.search(p)
            if m:
                year = m.group(1)
                continue

        if "RSVP by" in p:
            continue
        if "info@newhopecommunitybikes.com" in p:
            continue
        raise ValueError("Unknown line", p)


class TourDeCafeFacebook(scrapy.Spider):
    name = 'tour-de-cafe-newhope.fb'
    calendar_name = "Tour de Cafe, New Hope"

    allowed_domains = ["facebook.com", "www.facebook.com"]
    start_urls = ["https://www.facebook.com/groups/643937107228046/events"]

    def parse(self, response: Response) -> Iterator[Request]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        # the text we're looking for is embedded in a script tag. There's ~131. Find the right one.
        for _ in response.css("script"):
            if not all([
                _.attrib.get('type') == 'application/json',
                'data-content-len' in _.attrib,
                'data-sjs' in _.attrib,
            ]):
                continue

            json_text = _.css("::text").get()
            if json_text is None:
                continue

            loaded_json_object = json.loads(json_text)
            for facebook_event in extract_prefetched_events_from_inline_json(loaded_json_object):
                self.log(f"Discovered event {facebook_event.id=} {facebook_event.url=}")
                yield Request(url=facebook_event.url, callback=self.parse_single_event_page)

    def parse_single_event_page(self, response: Response) -> Iterator[Event]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        # debugging
        #from scrapy.utils.httpobj import urlparse_cached
        #parsed_url = urlparse_cached(response)
        #filename = f"debug-{parsed_url.path.replace("/", "-")}.html"
        #Path(filename).write_bytes(response.body)
        #self.log(f"Saved file {filename}")

        page_title = response.css("title::text").get(default="")

        event: Event | None = None
        start_datetime: datetime | None = None
        end_datetime: datetime | None = None

        for _ in response.css("script"):
            if not all([
                _.attrib.get('type') == 'application/json',
                'data-content-len' in _.attrib,
                'data-sjs' in _.attrib,
            ]):
                continue

            json_text = _.css("::text").get()
            if json_text is None:
                continue

            loaded_json_object = json.loads(json_text)

            prefetched_objects = list(extract_prefetched_objects_from_inline_json(loaded_json_object))

            for r in prefetched_objects:
                if r.graph_method_name == 'PublicEventCometAboutRootQuery':
                    result = RelayPrefetchedStreamCache_Result.from_bbox(r.bbox)
                    if result.path == ["event"] and 'start_timestamp' in result.data:

                        tzinfo = discover_zoneinfo_for_shortname(result.data["tz_display_name"])
                        # HACK: facebook returns timezone strings in shortform, like EST/EDT.
                        # Don't have a good way to do a reverse-lookup of a zoneinfo.ZoneInfo from the shortform.
                        # But RespectCyclists is based from Toronto, so realistically only going to see two timezone strings.
                        # Just map them.
                        #if result.data["tz_display_name"] in ('EST', 'EDT'):
                        #    tzinfo = ZoneInfo("America/Toronto")
                        #else:
                        #    raise ValueError(f"Unknown timezone {result.data['tz_display_name']}")

                        start_datetime = datetime.fromtimestamp(result.data["start_timestamp"], tzinfo)
                        end_datetime = datetime.fromtimestamp(result.data["end_timestamp"], tzinfo)
                        if result.data["end_timestamp"] == 0 or end_datetime < start_datetime:
                            self.logger.warning("No end timestamp, setting based on default duration")
                            end_datetime = start_datetime + ESTIMATED_DURATION

                    elif 'event' in result.data:
                        fb_event_object = FBEvent.from_dict(result.data["event"])
                        event = convert_facebook_event_to_spider_event(fb_event=fb_event_object)

        if event is None:
            raise ValueError("Failed to parse event from prefetched stream cache")

        event.summary = page_title
        if start_datetime is not None:
            event.start_datetime = start_datetime
        if end_datetime is not None:
            event.end_datetime = end_datetime
        event.url = response.url

        yield event


def convert_facebook_event_to_spider_event(fb_event: FBEvent) -> Event:
    description = str(fb_event.description)
    if fb_event.event_creator is not None:
        description += f"\nCreated by: {fb_event.event_creator.name}"
    if fb_event.is_past:
        description += "\nEvent is in the past."

    # Only date is available, so just stamp Noon.
    assumed_duration = timedelta(hours=1)
    if fb_event.start_date is not None:
        start_datetime = datetime.combine(fb_event.start_date, time(hour=12))
        end_datetime = start_datetime + assumed_duration
        description += "Check url for start time!"
    else:
        start_datetime = None
        end_datetime = None

    summary = f"{fb_event.name} - placeholder time"
    return Event(
        summary=summary,
        start_datetime=start_datetime,
        end_datetime=end_datetime,
        original_description=description,
        url=fb_event.url,
        location=None,
    )
