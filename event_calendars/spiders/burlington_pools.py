
import scrapy
from scrapy.http import HtmlResponse, TextResponse, Response
from scrapy.http.request.form import FormdataType
from ..items import BookableEvent


from datetime import date, datetime, timedelta
import dateutil

from typing import Iterable, Iterator


def _parse_date_time(formatted_date: str, formatted_time: str) -> datetime:
    return dateutil.parser.parse(f"{formatted_date} {formatted_time}")


DEFAULT_SEARCH = {
    'values[0][Name]': 'Keyword',
    'values[0][Value]': '',
    'values[0][Value2]': '',
    'values[0][ValueKind]': '9',

    'values[1][Name]': 'Date Range',
    'values[1][Value]': '%sT00:00:00.000Z' % date.today(),
    'values[1][Value2]': '%sT00:00:00.000Z' % (date.today() + timedelta(days=40)),
    'values[1][ValueKind]': '6',

    'values[2][Name]': 'Age',
    'values[2][Value]': '0',
    'values[2][Value2]': '1188',
    'values[2][ValueKind]': '0',
}

class BurlingtonPools(scrapy.Spider):
    name = "burlington-pools"
    calendar_name = "Burlington Pools"

    allowed_domains = ["cityofburlington.perfectmind.com"]

    calendarId = '598fc12b-1445-4708-8de3-4a997690a6a3'  # Swimming
    widgetId = 'ee6566f5-1e27-433c-9c19-86e76a0e3556'  # Drop-in?

    def start_requests(self) -> Iterable[scrapy.Request]:
        urls = [
            f"https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPages/Classes?calendarId={self.calendarId}&widgetId={self.widgetId}",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response) -> scrapy.FormRequest:
        assert isinstance(response, HtmlResponse)  # guard because signature of parse() doesn't declare `response`

        # this page contains a form with an Input element "__RequestVerificationToken" whose value must be included on subsequent requests
        verification_token = response.xpath('//form[@id="AjaxAntiForgeryForm"]/input[@name="__RequestVerificationToken"]/@value').get()
        if verification_token is None:
            raise RuntimeError("Failed to extract __RequestVerificationToken from form")

        form_request_kv_data: FormdataType = {
            'calendarId': self.calendarId,
            'widgetId': self.widgetId,
            'page': '0',
            **DEFAULT_SEARCH,
            '__RequestVerificationToken': verification_token
        }

        return scrapy.FormRequest(
            url='https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPagesV2/ClassesV2',
            formdata=form_request_kv_data,
            callback=self.parse_classes_v2_json,
            cb_kwargs={
                'verification_token': verification_token
            },
        )

    def parse_classes_v2_json(self, response: TextResponse, verification_token: str) -> Iterator[BookableEvent | scrapy.FormRequest]:
        payload = response.json()
        #assert isinstance(self.crawler.stats, StatsCollector)  # TODO: just generate in Dataclass?

        for c in payload['classes']:

            b = BookableEvent(
                summary = str.strip(c['EventName']),

                start_datetime = _parse_date_time(c['FormattedStartDate'], c['FormattedStartTime']),
                end_datetime = _parse_date_time(c['FormattedEndDate'], c['FormattedEndTime']),
                #updated_at = self.crawler.stats.get_value('start_time'),  # TODO: Dataclass property?

                #  Address: {'AddressTag': 'Centennial Pool', 'Street': '5151 New Street', 'City': 'Burlington', 'PostalCode': 'L7P 4J5', 'CountryId': 0, 'Country': '', 'StateProvinceId': 0, 'AnyFieldMissing': True, 'Latitude': 43.37193, 'Longitude': -79.750327, 'Id': '1caa5785-bc69-469c-ac36-5ae3758860d3'}
                location = f"{c['Address']['AddressTag']}, {c['Address']['Street']}, {c['Address']['City']}, {c['Address']['PostalCode']}",

                original_description = str.strip(c['Details']),

                # instructor = c['Instructor']['FullName'] or None,
                #location = str.strip(c['Location'])
                facility = str.strip(c['Facility']),
                price_range = c['PriceRange'] or None,
                spots_remaining = c['Spots'] or None,
                url = f'https://cityofburlington.perfectmind.com/22818/Clients/BookMe4LandingPages/Class?widgetId={self.widgetId}&redirectedFromEmbededMode=False&classId={c["EventId"]}&occurrenceDate={c["OccurrenceDate"]}',

                category=None,
            )
            yield b

        if payload['nextKey'] and payload['nextKey'] != "0001-01-01":
            yield scrapy.FormRequest(
                url='https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPagesV2/ClassesV2',
                formdata={
                    'calendarId': self.calendarId,
                    'widgetId': self.widgetId,
                    'page': '0',
                    **DEFAULT_SEARCH,
                    'after': payload['nextKey'],
                    '__RequestVerificationToken': verification_token
                },
                callback=self.parse_classes_v2_json,
                cb_kwargs={
                    'verification_token': verification_token
                },
            )
