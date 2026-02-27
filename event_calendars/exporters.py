from collections.abc import Sequence
from io import BytesIO
from logging import getLogger
from pathlib import Path
from typing import Any

import icalendar
from scrapy import Spider
from scrapy.exporters import BaseItemExporter
from scrapy.spiderloader import get_spider_loader
from scrapy.utils.project import get_project_settings

from .items import Event

logger = getLogger(__name__)


def uri_params(params: dict[str, Any], spider: Spider | type[Spider]) -> dict[str, Any]:
    """Add spider_name to available uri_params template, so %(spider_name)s is usable in feed URIs."""
    return {
        **params,
        "spider_name": spider.name,
    }


def get_spider_from_export_filename(opened_filename: str) -> type[Spider]:
    """
    each spider gets its own file, but there's no indication of which spider this one is.
    go look it up by introspecting the filename.
    this must match the feed export in settings.py
    'out/%(spider_name)s.ical'

    This cannot work with batch options that change the filename.

    Simplied logic from scrapy.extensions.feedexport.FeedExporter.open_spider
    """

    project_settings = get_project_settings()
    spider_loader = get_spider_loader(project_settings)

    configured_feeds: Sequence[str] = list(project_settings.getdict("FEEDS", {}).keys())

    for spider_name in spider_loader.list():
        # get the hypothetical produced uri_params for this spider
        spider_cls: type[Spider] = spider_loader.load(spider_name)
        params = uri_params({}, spider_cls)

        # see if the opened_filename matches one of the hypothetical uri's produced from the configured patterns & params
        for output_filename_pattern in configured_feeds:
            uri: str = output_filename_pattern % params
            if uri == opened_filename:
                return spider_cls

    raise ValueError(f"Spider not found for {opened_filename=}")


class ICalItemExporter(BaseItemExporter):
    # similar to the XML exporter

    logger = getLogger(__name__)

    def __init__(self, file: BytesIO, **kwargs: Any) -> None:
        self.file = file  # already-open file handle

        try:
            spider_class = get_spider_from_export_filename(self.file.name)
            self.calendar_name = getattr(spider_class, "calendar_name")
        except (ValueError, AttributeError) as e:
            self.logger.warning(f"Unable to find calendar_name for {self.file.name=}: {e=}")
            self.calendar_name = Path(self.file.name).stem.replace("-", " ").title()

        super().__init__(**kwargs)

    def start_exporting(self) -> None:
        self.cal = icalendar.Calendar()
        self.cal.prodid = icalendar.vText("-//event-calendars//verselogic.net//")
        self.cal.version = icalendar.vText("2.0")
        self.cal.method = "PUBLISH"
        self.cal.calendar_name = self.calendar_name

    def export_item(self, item: Event) -> None:
        e = icalendar.Event()

        e.summary = item.summary
        e.uid = item.uid

        e.DTSTART = item.start_datetime
        e.DTEND = item.end_datetime
        e.DTSTAMP = item.updated_at

        e.url = item.url
        e.location = item.location
        e.description = item.description

        self.cal.add_component(e)

    def finish_exporting(self) -> None:
        self.cal.add_missing_timezones()
        """
        Stable ordering of output. Sort top-level sub-components by their UID property, if present.
        Components without a UID property (eg timezone info) are sorted first.
        Properties are sorted during write.
        """
        self.cal.subcomponents = sorted(self.cal.subcomponents, key=lambda e: e.get("UID", e.get("DTSTART", "0")))
        self.file.write(self.cal.to_ical(sorted=True))
