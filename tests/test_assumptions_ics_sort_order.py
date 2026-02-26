from datetime import datetime
from io import BytesIO
from textwrap import dedent
from uuid import uuid5

import icalendar


def test_assumption_icalendar_sortable_keys() -> None:
    a = icalendar.Calendar()
    a.prodid = '-//author.example.com//'
    a.version = '2.0'
    a.method = 'PUBLISH'
    a.calendar_name = "Cal Name"

    assert a.to_ical().decode() == dedent(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//author.example.com//
        METHOD:PUBLISH
        NAME:Cal Name
        END:VCALENDAR
        """
    ).replace("\n", "\r\n").lstrip()

    for component in "aZbYcWdXe":
        # create a hyper minimal event consisting only of a UID property, used as the sort key
        e = icalendar.Event()
        e.uid = icalendar.vText('uuid-'+component.upper())
        a.add_component(e)

    a.add_missing_timezones()
    baked_ical_file_content_unordered: str = a.to_ical().decode()

    # subcomponent items are sortable after insertion
    b = icalendar.Calendar.from_ical(baked_ical_file_content_unordered)
    b.subcomponents = sorted(b.subcomponents, key=lambda e: e.get("UID"))
    baked_ical_file_content_ordered: str = b.to_ical().decode()

    assert baked_ical_file_content_ordered == dedent(
        """
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//author.example.com//
        METHOD:PUBLISH
        NAME:Cal Name
        BEGIN:VEVENT
        UID:uuid-A
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-B
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-C
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-D
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-E
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-W
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-X
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-Y
        END:VEVENT
        BEGIN:VEVENT
        UID:uuid-Z
        END:VEVENT
        END:VCALENDAR
        """
    ).replace("\n", "\r\n").lstrip()


def test_ICalItemExporter_sorts() -> None:
    from event_calendars.exporters import ICalItemExporter
    from event_calendars.items import Event, ns

    writer_file = BytesIO()
    writer_file.name = "fake-filename-used-for-calendar-name"
    exporter = ICalItemExporter(writer_file)

    exporter.start_exporting()

    _fake_date = datetime.fromisoformat("2020-01-01T13:30:00Z")  # needed by exporter but unimportant

    expected_uids: list[str] = []

    for letter in "aZbYcWdXe":
        expected_uids.append(str(uuid5(ns, letter)))
        item = Event(
            summary=letter,
            url=letter,  # sort key is uuid5(url)
            start_datetime=_fake_date,
            end_datetime=_fake_date,
            location="",
            original_description="",
        )
        exporter.export_item(item)
    exporter.finish_exporting()

    expected_uids_ordered = sorted(expected_uids)

    b = icalendar.Calendar.from_ical(writer_file.getvalue().decode())
    for (left, right) in zip(expected_uids_ordered, b.events):
        assert left == right.get("UID")
