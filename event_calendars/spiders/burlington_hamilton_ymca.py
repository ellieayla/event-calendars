from typing import Iterable
import scrapy
from scrapy.http import TextResponse, Response



from ..items import BookableEvent

from datetime import datetime
import dateutil
import dateutil.tz



# TODO: Maybe this should be split
class YmcaHamiltonBurlingtonPools(scrapy.Spider):
    name = "ymca-hamilton-burlington"
    allowed_domains = ["www.ymcahbb.ca"]

    def start_requests(self) -> Iterable[scrapy.Request]:

        locations = [
            "Ron%20Edwards%20Family%20YMCA",
            "Hamilton%20Downtown%20Family%20YMCA",
            # "Flamborough%20Family%20YMCA",
            # "Laurier%20Brantford%20YMCA",
            # "Les%20Chater%20Family%20YMCA",
        ]

        # next 30 days
        dates = list([d.date() for d in dateutil.rrule.rrule(dateutil.rrule.DAILY, count=30, dtstart=datetime.now())])

        urls = [
            f"https://www.ymcahbb.ca/schedules/get-event-data/{loc}/0/{d}"
            for loc in locations
            for d in dates
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_json_classlist)

    def parse_json_classlist(self, response: Response) -> Iterable[BookableEvent]:
        if not isinstance(response, TextResponse):
            raise ValueError("Non-text response")
        payload = response.json()

        for c in payload:

            """
            {
                'category': 'Lane Swim',
                'class': '80402',
                'class_info': {'description': '',
                                'nid': '80402',
                                'path': 'https://www.ymcahbb.ca/programs/health-and-fitness/group-exercises/lane-swim/class-times?location=8855?location=8855',
                                'title': 'Lane Swim'},
                'duration': '330',
                'duration_hours': 5,
                'duration_minutes': 30,
                'end_timestamp': '1718298000',
                'instructor': None,
                'location': 'Ron Edwards Family YMCA',
                'location_info': {'address': '500 Drury Lane, Burlington, ON, CA, L7R 2X2',
                                'days': [['Mon - Fri:', '6:00am - 9:30pm'],
                                            ['Sat:', '8:00am - 5:30pm'],
                                            ['Sun:', '8:00am - 4:00pm']],
                                'email': 'burlington.membership@ymcahbb.ca',
                                'nid': '8855',
                                'phone': '905-632-5000',
                                'title': 'Ron Edwards Family YMCA'},
                'name': 'Lane Swim - Ron Edwards - Thursday 7:30 AM',
                'nid': '101566',
                'productid': None,
                'register_text': 'Drop-in Program',
                'register_url': 'route:<nolink>',
                'room': None,
                'session': '101566',
                'start_timestamp': '1718278200',
                'time_end': '1:00PM',
                'time_end_calendar': '2024-06-13 13:00:00',
                'time_start': '7:30AM',
                'time_start_calendar': '2024-06-13 07:30:00',
                'time_start_sort': '0730',
                'timezone': 'America/Toronto'
            }
            """
            b = BookableEvent(
                summary = c['name'],

                start_datetime = dateutil.parser.parse(c['time_start_calendar'] + " LTZ", tzinfos={"LTZ": dateutil.tz.gettz(c['timezone'])}),
                end_datetime = dateutil.parser.parse(c['time_end_calendar'] + " LTZ", tzinfos={"LTZ": dateutil.tz.gettz(c['timezone'])}),

                location = f"{c['location']}, {c['location_info']['address']}",
                url = c['register_url'] if c['register_url'] != 'route:<nolink>' else None,

                original_description = c['class_info']['title'] + "\n" + c['class_info']['description'],

                facility = c['location'],
                category = c['category'],
            )
            yield b
