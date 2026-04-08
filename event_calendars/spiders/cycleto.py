from collections.abc import Iterator

import datauri
import icalendar
import scrapy
import scrapy.http
from scrapy.exceptions import CloseSpider

from ..items import Event
from ..text_content import readable_text_content


class CycleToronto(scrapy.Spider):
    name = "cycle-toronto"
    calendar_name = "Cycle TO"

    allowed_domains = ["www.cycleto.ca"]
    start_urls = ["https://www.cycleto.ca/events"]

    def parse(self, response: scrapy.http.Response) -> Iterator[scrapy.Request]:
        for event_url in response.css(".calendar-list li.calendar-day-events-event a::attr(href)").getall():
            yield scrapy.Request(
                url=response.urljoin(event_url),
                callback=self.parse_details_page,
            )

    def parse_details_page(self, response: scrapy.http.Response) -> Event:
        ics_blob = response.xpath('//a[contains(@download, "event.ics")]/@href').get()
        if ics_blob is None:
            raise CloseSpider(f"Failed to extract ICS Blob from {response.url}")

        a: datauri.datauri.ParsedDataURI = datauri.parse(ics_blob)  # untyped, datauri typestubs in root of project repo
        base_calendar: icalendar.Calendar = icalendar.Calendar.from_ical(a.data, multiple=False)
        base_event = base_calendar.events[0]

        summary = base_event.decoded("summary").removesuffix(" - Cycle Toronto")
        start_time = base_event.decoded("dtstart")
        end_time = base_event.decoded("dtend")
        location = base_event.decoded("location")
        url = base_event.decoded("url")

        description = readable_text_content(response.css("main div.text-content.inner-block")[0].root)

        return Event(
            summary=summary,
            start_datetime=start_time,
            end_datetime=end_time,
            url=url,
            location=location,
            original_description=description,
        )
