import scrapy
from scrapy.http import Response, HtmlResponse, Request

from ..items import Event

from event_calendars.fb_graphql import extract_prefetched_events_from_inline_json
from event_calendars.fb_graphql import extract_prefetched_objects_from_inline_json
from event_calendars.fb_graphql import Event as FBEvent
from event_calendars.fb_graphql import RelayPrefetchedStreamCache_Result

import json
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from typing import Iterator

class RespectCyclistsFacebookEvents(scrapy.Spider):
    name = "respect_cyclists_facebook"
    allowed_domains = ["facebook.com", "www.facebook.com"]
    start_urls = ["https://www.facebook.com/groups/respectcyclists/events"]

    def parse(self, response: Response) -> Iterator[Event | Request]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        # debugging
        #from scrapy.utils.httpobj import urlparse_cached
        #parsed_url = urlparse_cached(response)
        #filename = f"debug-{parsed_url.path.replace("/", "-")}.html"
        #Path(filename).write_bytes(response.body)
        #self.log(f"Saved file {filename}")

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
                # yield convert_facebook_event_to_spider_event(facebook_event)  # could make a crummy event from the list
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
                        # HACK: facebook returns timezone strings in shortform, like EST/EDT.
                        # Don't have a good way to do a reverse-lookup of a zoneinfo.ZoneInfo from the shortform.
                        # But RespectCyclists is based from Toronto, so realistically only going to see two timezone strings.
                        # Just map them.
                        if result.data["tz_display_name"] in ('EST', 'EDT'):
                            tzinfo = ZoneInfo("US/Eastern")
                        else:
                            raise ValueError(f"Unknown timezone {result.data['tz_display_name']}")

                        start_datetime = datetime.fromtimestamp(result.data["start_timestamp"], tzinfo)
                        end_datetime = datetime.fromtimestamp(result.data["end_timestamp"], tzinfo)

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
