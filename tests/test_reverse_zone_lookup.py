from zoneinfo import ZoneInfo

import pytest

from event_calendars.timezone_lookup import discover_zoneinfo_for_shortname


@pytest.mark.parametrize(
    "tzname,zoneinfo",
    [
        ("EDT", ZoneInfo("America/Toronto")),
        ("EST", ZoneInfo("America/Toronto")),
    ],
)
def test_lookup_zone(tzname: str, zoneinfo: ZoneInfo) -> None:
    y = discover_zoneinfo_for_shortname(tzname)
    assert y == zoneinfo


def test_lookup_caches() -> None:
    tzname = "EST"

    discover_zoneinfo_for_shortname.cache_clear()

    discover_zoneinfo_for_shortname(tzname)

    i = discover_zoneinfo_for_shortname.cache_info()
    assert i.currsize == 1
    assert i.misses == 1
    assert i.hits == 0

    discover_zoneinfo_for_shortname(tzname)
    i = discover_zoneinfo_for_shortname.cache_info()
    assert i.hits == 1
