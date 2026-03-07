import logging
import re
from collections.abc import Iterator, Sequence
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import dateutil
import scrapy
from scrapy.exceptions import DropItem
from scrapy.http import HtmlResponse, Response

from event_calendars.utils import readable_text_content

from ..items import Event

BURLINGTON_TIMEZONE = ZoneInfo("America/Toronto")
DEFAULT_DURATION = timedelta(hours=2)


class BurlingtonGreen(scrapy.Spider):
    name = "burlington-green"
    calendar_name = "Burlington Green"

    allowed_domains = ["www.burlingtongreen.org"]
    start_urls = ["https://www.burlingtongreen.org/events/"]

    def parse(self, response: Response) -> Iterator[scrapy.Request]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        for e in response.css("div.elementor div a::attr(href)").getall():
            yield scrapy.Request(
                response.urljoin(e),
                callback=self.parse_event_details,
            )

    def parse_event_details(self, response: Response) -> Iterator[Event]:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        logger = logging.getLogger(self.name).getChild(response.url)
        # one event, like https://www.burlingtongreen.org/events/get-ready-for-community-clean-up/

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
            start_datetime, end_datetime = extract_dates_from_description(description)
            logger.info(f"Extracted {start_datetime=} {end_datetime=} from description")
        except ValueError as e:
            logger.warning(e)

        try:
            start_datetime, end_datetime = extract_dates_from_metadata([item.get() for item in header_metadata_items])
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
        print(f"{ev=} has {location=}")
        yield ev


def extract_location_from_description(description: str) -> str | None:
    AT_RE = re.compile(r"(location| at ):? *(?P<place>[^\.]+)")
    for row in description.splitlines():
        # if row.lower().startswith(LOC_HEADER):
        #    return row[len(LOC_HEADER):].strip()

        m = AT_RE.search(row)
        if m:
            return m.group("place").strip()

    return None


def extract_dates_from_description(description: str) -> tuple[datetime, datetime | None]:
    start_date: date | None = None
    start_time: time = time(hour=0, minute=0, tzinfo=BURLINGTON_TIMEZONE)
    end_date: date | None = None
    end_time: time | None = None

    description = description.replace("\u2013", "-")  # fancy hyphen

    RE_COLON_ITEM = re.compile(r"(?P<key>\w{1,15}): *(?P<value>.*)")
    RE_URL = re.compile(r"\(https?://\w+?\)", re.IGNORECASE)

    RE_TIME_RANGE = re.compile(r"(?P<lead>.*) (?P<left>\d\d?(:\d\d)?) *(-|to) *(?P<right>\d\d?(:\d\d)?) (?P<trail>.*)")

    for possible_date in description.splitlines():
        if "today" in possible_date.lower():
            continue  # skip the donation request

        m = RE_TIME_RANGE.match(possible_date)
        if m:
            a_string = f"{m.group('lead')} {m.group('left')} {m.group('trail')}"
            b_string = f"{m.group('lead')} {m.group('right')} {m.group('trail')}"

            try:
                _start_datetime, _ = extract_dates_from_description(a_string)
                _end_datetime, _ = extract_dates_from_description(b_string)

                if _start_datetime >= _end_datetime:
                    _start_datetime = _start_datetime - timedelta(hours=12)
                return (_start_datetime, _end_datetime)
            except ValueError:
                pass  # that didn't work, carry on with detection

        m = RE_COLON_ITEM.match(possible_date)
        if m:
            match m.group("key").lower():
                case "date":
                    start_date = dateutil.parser.parse(m.group("value"))
                    logging.getLogger().debug(f"Found start date in description key: {possible_date=} {start_date=}")
                    continue
                case "time":
                    start_time = dateutil.parser.parse(m.group("value")).time().replace(tzinfo=BURLINGTON_TIMEZONE)
                    continue
                case _:
                    pass

        try:
            simple_description = RE_URL.sub("", possible_date)
            # print(f"{possible_date=} {simple_description=}")
            _start_datetime = dateutil.parser.parse(simple_description, fuzzy=True)
            start_date = _start_datetime.date()
            start_time = _start_datetime.time().replace(tzinfo=BURLINGTON_TIMEZONE)

            logging.getLogger().debug(f"Found start date in description body: {possible_date=} {start_date=}")
        except dateutil.parser.ParserError:
            pass

    if start_date is None:
        raise ValueError("Failed to find a start date in description")

    start_datetime: datetime = datetime.combine(start_date, start_time)
    end_datetime = None
    if end_time:
        if end_date:
            end_datetime = datetime.combine(end_date, end_time)
        else:
            end_datetime = datetime.combine(start_date, end_time)

    return (start_datetime, end_datetime)


def extract_dates_from_metadata(header_metadata_items: Sequence[str]) -> tuple[datetime, datetime | None]:
    start_date: date | None = None
    start_time: time = time(hour=0, minute=0, tzinfo=BURLINGTON_TIMEZONE)
    end_date: date | None = None
    end_time: time | None = None

    for header_text in header_metadata_items:
        if " : " in header_text:
            header_text = header_text.replace(" : ", ":")

        try:
            (found_date_chunk, leftover_tokens) = dateutil.parser.parse(header_text, fuzzy_with_tokens=True)
            found_date_chunk = found_date_chunk.replace(tzinfo=BURLINGTON_TIMEZONE)
            simple_header_text = "".join(leftover_tokens).lower()
        except dateutil.parser.ParserError:
            continue

        logging.getLogger().debug(f"Found {found_date_chunk} in {header_text=}")
        if "time" in simple_header_text:
            if "end" in simple_header_text:
                end_time = found_date_chunk.time().replace(tzinfo=BURLINGTON_TIMEZONE)
            else:
                start_time = found_date_chunk.time().replace(tzinfo=BURLINGTON_TIMEZONE)
        else:
            if "end" in simple_header_text:
                end_date = found_date_chunk.date()
            else:
                start_date = found_date_chunk.date()

    if start_date is None:
        raise ValueError("Failed to find a start date in metadata")

    start_datetime = datetime.combine(start_date, start_time)

    if end_time:
        if end_date:
            end_datetime = datetime.combine(end_date, end_time)
        else:
            end_datetime = datetime.combine(start_date, end_time)
    elif end_date:
        end_datetime = datetime.combine(end_date, time(hour=0, minute=0, tzinfo=BURLINGTON_TIMEZONE))
    else:
        end_datetime = None

    return (start_datetime, end_datetime)
