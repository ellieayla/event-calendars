from collections.abc import Iterator
from datetime import datetime, timedelta

import datauri
import icalendar
import scrapy
import scrapy.http
from scrapy.exceptions import CloseSpider

from ..items import Event
from ..utils import readable_text_content


class CycleToronto(scrapy.Spider):
    name = 'cycle-toronto'
    calendar_name = "Cycle TO"

    allowed_domains = ['www.cycleto.ca', 'web.archive.org']
    start_urls = ['https://www.cycleto.ca/events']

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        for event_url in response.css(".calendar-list li.calendar-day-events-event a::attr(href)").getall():
            yield scrapy.Request(
                url=event_url,
                callback=self.parse_details_page,
            )

    def _parse_from_events_list_directly(self, response: scrapy.http.Response) -> Iterator[Event]:
        # instead of fetching details from the event page (which might not be fetchable),
        # just make a short summary from the information available in the events list here.

        for e in response.css(".calendar-list li.calendar-day-events-event"):
            summary = e.css(".calendar-day-events-event-headline::text").extract_first("").strip()
            start_time = datetime.fromisoformat(e.css("time").attrib['datetime'].strip())
            end_time = start_time + timedelta(hours=1)

            url_fragment: str = e.css("a::attr(href)").extract_first("")
            if response.meta.get('wayback_request'):
                event_url = url_fragment.split("/", maxsplit=3)[3]
            else:
                event_url = response.urljoin(url_fragment)

            yield Event(
                summary=summary,
                url=event_url,
                start_datetime=start_time,
                end_datetime=end_time,
                location=None,
            )

    def parse_details_page(self, response: scrapy.http.Response) -> Iterator[Event]:
        ics_blob = response.xpath('//a[contains(@download, "event.ics")]/@href').get()
        if ics_blob is None:
            raise CloseSpider(f"Failed to extract ICS Blob from {response.url}")

        a: datauri.datauri.ParsedDataURI = datauri.parse(ics_blob)  # untyped, datauri typestubs in root of project repo
        base_calendar: icalendar.Calendar = icalendar.Calendar.from_ical(a.data, multiple=False)
        base_event = base_calendar.events[0]

        summary = base_event.decoded('summary').removesuffix(" - Cycle Toronto")
        start_time = base_event.decoded('dtstart')
        end_time = base_event.decoded('dtend')
        location = base_event.decoded("location")
        url = base_event.decoded('url')

        description = readable_text_content(
            response.css("main div.text-content.inner-block")[0].root
        )

        yield Event(
            summary=summary,
            start_datetime=start_time,
            end_datetime=end_time,
            url=url,
            location=location,
            original_description=description,
        )
