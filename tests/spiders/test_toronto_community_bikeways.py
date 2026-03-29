from pathlib import Path

import pytest
from scrapy import Request
from scrapy.http import HtmlResponse, TextResponse

from event_calendars.items import Event
from event_calendars.spiders.toronto_community_bikeways import TorontoCommunityBikeways

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


community_bikeways_toronto_example_ical_file = r"""
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Squarespace Inc/Squarespace 6//v6//EN
BEGIN:VEVENT
UID:697bdc0552e067763b3704e0@squarespace.com
DTSTAMP:20260129T222239Z
DTSTART:20260211T000000Z
DTEND:20260211T010000Z
SUMMARY:E-bikes
URL:https://example.com/mismatched-url
GEO:0.0;0.0
LOCATION:Curbside
END:VEVENT
END:VCALENDAR
"""

def test_merge_with_ical_file_mismatched_url() -> None:
    response: TextResponse = TextResponse(
        url='https://example.com/document.ics',
        status=200,
        headers={"content-type": "text/calendar"},
        body=community_bikeways_toronto_example_ical_file,
        encoding="utf-8",
    )
    s: TorontoCommunityBikeways = TorontoCommunityBikeways()
    event: Event = s.handle_ical_file(
        response=response,
        event_url='https://example.com',
        description='blah',
    )

    assert event.url == 'https://example.com'  # page wins
    assert event.description == "blah\nURL: https://example.com"
    assert event.location == "Curbside"
    assert event.summary == "E-bikes"


@pytest.mark.datafiles(FIXTURE_DIR / "communitybikewaysto.ca-events.html")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "communitybikewaysto.ca-events.html").read_bytes()

    spider = TorontoCommunityBikeways()
    response = HtmlResponse(url=spider.start_urls[0], status=200, body=html)

    results = list(spider.parse(response))

    for _ in results:
        assert isinstance(_, Request)

    assert results[0].url == "https://www.communitybikewaysto.ca/events/the-future-of-e-bikes-community-bikeways-fix"


@pytest.mark.datafiles(FIXTURE_DIR / "communitybikewaysto.ca-event-west-scarborough.html")
def test_parse_single_event_page_for_ics_url(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "communitybikewaysto.ca-event-west-scarborough.html").read_bytes()

    spider = TorontoCommunityBikeways()
    response = HtmlResponse(url="https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp", status=200, body=html)

    request: Request = spider.parse_meeting_details(response)

    assert request.url == "https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp?format=ical"
    assert request.cb_kwargs["event_url"] == "https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp"
    assert "westscarboroughrailpath.ca" in request.cb_kwargs["description"]



@pytest.mark.datafiles(FIXTURE_DIR / "communitybikewaysto.ca-event-west-scarborough.html")
def test_unreadable_description(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "communitybikewaysto.ca-event-west-scarborough.html").read_bytes()

    spider = TorontoCommunityBikeways()
    response = HtmlResponse(url="https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp", status=200, body=html)

    response.css(".events-item .html-block").drop()  # wipe out the description

    request: Request = spider.parse_meeting_details(response)

    assert "" == request.cb_kwargs["description"]


@pytest.mark.datafiles(FIXTURE_DIR / "communitybikewaysto.ca-event-west-scarborough.ics")
def test_parse_single_event_ics_file(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html: bytes = (datafiles / "communitybikewaysto.ca-event-west-scarborough.ics").read_bytes()

    spider = TorontoCommunityBikeways()
    response = HtmlResponse(url="https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp?format=ical", status=200, body=html)

    event: Event = spider.handle_ical_file(response, event_url="https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp", description="example-description")

    assert event.url == "https://www.communitybikewaysto.ca/events/west-scarborough-rail-path-wsrp"
    assert event.description == f"example-description\nURL: {event.url}"
    assert event.location == "Albert Campbell Library, 496 Birchmount Road, Toronto, ON, M1K 1N8, Canada"
    assert event.summary == "West Scarborough Rail Path (WSRP)"
