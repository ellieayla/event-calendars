from datetime import datetime, time
from pathlib import Path
from typing import LiteralString
from zoneinfo import ZoneInfo

import pytest

from event_calendars.text_content import extract_dates_from_description, extract_location_from_description

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"

TODAY = datetime.now()
CUR_YEAR = TODAY.year
EASTERN = ZoneInfo("America/Toronto")


@pytest.mark.parametrize(
    "desc, s, e",
    [
        ("March 12th\nDate: March 13", datetime(year=CUR_YEAR, month=3, day=13, tzinfo=EASTERN), None),
        ("firstline\nSomething on Thursday, March 12th, from 7:00–8:15 pm on whatever.\n\nNextline", datetime(year=CUR_YEAR, month=3, day=12, hour=19, minute=0, tzinfo=EASTERN), datetime(year=CUR_YEAR, month=3, day=12, hour=20, minute=15, tzinfo=EASTERN)),
        ("firstline\nSomething on Thursday, March 12th 2021, from 7:00-8:15 pm on whatever.\n\nNextline", datetime(year=2021, month=3, day=12, hour=19, minute=0, tzinfo=EASTERN), datetime(year=2021, month=3, day=12, hour=20, minute=15, tzinfo=EASTERN)),
        ("it's 7 - 8 pm.", datetime.combine(TODAY, time(19), tzinfo=EASTERN), datetime.combine(TODAY, time(20), tzinfo=EASTERN)),
        ("it's 11 - 1 pm.", datetime.combine(TODAY, time(11), tzinfo=EASTERN), datetime.combine(TODAY, time(13), tzinfo=EASTERN)),
        ("it's 11 am", datetime.combine(TODAY, time(11), tzinfo=EASTERN), None),
        ("it's 1 - 1 pm.", datetime.combine(TODAY, time(1), tzinfo=EASTERN), datetime.combine(TODAY, time(13), tzinfo=EASTERN)),
        ("it's 3 to 4 pm.", datetime.combine(TODAY, time(15), tzinfo=EASTERN), datetime.combine(TODAY, time(16), tzinfo=EASTERN)),
    ],
)
def test_parse_time_range_from_description(desc: LiteralString, s: datetime, e: datetime) -> None:
    """Sometimes people write times like 11-3. Extract useful datetime objects from that."""
    got_s, got_e = extract_dates_from_description(desc, default_tzinfo=EASTERN)

    assert (s, e) == (got_s, got_e)

@pytest.mark.parametrize(
    "desc",
    [
        "location: here ",
        "location:here",
        "meet at here."
    ],
)
def test_extract_location(desc: LiteralString) -> None:
    assert "here" == extract_location_from_description(desc)
