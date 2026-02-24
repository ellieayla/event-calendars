from collections.abc import Iterator

from scrapy.http import TextResponse

from event_calendars.items import Event
from event_calendars.spiders.toronto_community_bikeways import TorontoCommunityBikeways

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
GEO:0.0;0.0
LOCATION:Curbside
END:VEVENT
END:VCALENDAR
"""

def test_merge_with_ical_file() -> None:
    response: TextResponse = TextResponse(
        url='https://example.com/document.ics',
        status=200,
        headers={"content-type": "text/calendar"},
        body=community_bikeways_toronto_example_ical_file,
        encoding='utf-8',
    )
    s: TorontoCommunityBikeways = TorontoCommunityBikeways()
    g: Iterator[Event] = s.handle_ical_file(
        response=response,
        event_url='https://example.com',
        description='blah',
    )
    yielded_event = next(g)
    assert isinstance(yielded_event, Event)

    assert yielded_event.url == 'https://example.com'
    assert yielded_event.description == "blah\nURL: https://example.com"
    assert 'Curbside' == yielded_event.location
    assert 'E-bikes' == yielded_event.summary
