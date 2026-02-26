from event_calendars.exporters import get_spider_from_export_filename
from event_calendars.spiders.newhope import TourDeCafe


def test_get_spider_from_export_filename() -> None:

    spider_class = get_spider_from_export_filename("out/tour-de-cafe-newhope.ical")

    assert spider_class is TourDeCafe
