from typing import LiteralString

import pytest

from event_calendars.text_content import extract_location_from_description


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
