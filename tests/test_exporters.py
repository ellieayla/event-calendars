import io
from pathlib import Path

import pytest

from event_calendars.exporters import ICalItemExporter, get_spider_from_export_filename
from event_calendars.spiders.newhope import TourDeCafe


def test_get_spider_from_export_filename() -> None:
    """Look up a Spider class by output filename."""
    spider_class = get_spider_from_export_filename("out/tour-de-cafe-newhope.ical")

    assert spider_class is TourDeCafe


def test_unable_to_get_spider_for_unknown_filename() -> None:
    with pytest.raises(ValueError):
        get_spider_from_export_filename("out/DOESNOTEXIST.ical")


def test_no_name_from_export_file_handle(tmp_path: Path ) -> None:
    """Exporter generates a calendar_name from filename on failed Spider class lookup."""

    file = io.BytesIO()
    file.name = "out/DOESNOTEXIST.ical"

    export = ICalItemExporter(file=file)
    assert export.calendar_name == "Doesnotexist"


def test_name_from_export_file_handle(tmp_path: Path ) -> None:
    """Exporter uses the associated spider.calendar_name when it can lookup a Spider class."""

    file = io.BytesIO()
    file.name = "out/httpbin.ical"

    export = ICalItemExporter(file=file)
    assert export.calendar_name == "The Exceptional httpbin.org"
