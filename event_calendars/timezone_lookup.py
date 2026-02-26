from datetime import datetime
from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones


def _common_timezone_name_sortkey(tzname: str) -> int:
    """
    Sort timezones likely to be used closer to the top, so loading them is faster.
    Most of these calendars are for organizations near Toronto, so prioritize that.
    Keep all other known timezone names in the list.
    """
    if tzname == 'America/Toronto':
        return 0
    if tzname.startswith("US/"):
        return 5
    if tzname.startswith("Etc/"):
        return 7
    return 9


@lru_cache(maxsize=5)
def discover_zoneinfo_for_shortname(tzname: str) -> ZoneInfo:
    """
    Load a ZoneInfo object which corrosponds to a tzname shortname for the zone.

    zoneinfo.ZoneInfo(key) finds the key in the IANA time zone database, like America/Toronto
    zoneinfo.ZoneInfo(key).tzname() returns a short name for that zone, like EDT or EST.

    Sometimes published events *only* contain the short tzname.

    Load many zones, searching for one that's suitable.
    """

    # A ZoneInfo.tzname() may produce different strings depending on the date passed in.
    # Pass in 3 magic values, in hopes of straddling all possible names.
    now = datetime.now()
    january = datetime(2026, 1, 1)
    june = datetime(2026, 6, 1)

    for zone_name in sorted(available_timezones(), key=_common_timezone_name_sortkey):
        zi: ZoneInfo = ZoneInfo(zone_name)
        if any([zi.tzname(dt) == tzname for dt in (now, january, june)]):
            return zi

    raise ZoneInfoNotFoundError(f'No time zone found with key {tzname}')
