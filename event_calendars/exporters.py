
from io import BytesIO
from pathlib import Path
from typing import Any

import icalendar
from scrapy import Spider
from scrapy.exporters import BaseItemExporter

from .items import Event


def uri_params(params: dict[str, Any], spider: Spider) -> dict[str, Any]:
    """Add spider_name to available uri_params template, so %(spider_name)s is usable in feed URIs."""
    return {
        **params,
        "spider_name": spider.name,
    }


class ICalItemExporter(BaseItemExporter):
    # similar to the XML exporter
    def __init__(self, file: BytesIO, **kwargs: Any) -> None:
        self.file = file  # already-open file handle
        self.calendar_name = Path(self.file.name).stem.replace("-", " ").title()
        super().__init__(**kwargs)

    def start_exporting(self) -> None:
        self.cal = icalendar.Calendar()
        self.cal.prodid = icalendar.vText('-//event-calendars//verselogic.net//')
        self.cal.version = icalendar.vText('2.0')
        self.cal.method = 'PUBLISH'
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
        self.cal.subcomponents = sorted(self.cal.subcomponents, key=lambda e: e.get("UID", "0"))
        self.file.write(self.cal.to_ical(sorted=True))
