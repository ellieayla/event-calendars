# See documentation in:
# https://docs.scrapy.org/en/latest/topics/download-handlers.html#writing-your-own-download-handler

from typing import Self
from waybackpy import WaybackMachineAvailabilityAPI, WaybackMachineSaveAPI
from waybackpy.exceptions import ArchiveNotInAvailabilityAPIResponse

from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.http import Response
from scrapy.exceptions import NotConfigured, CloseSpider
from scrapy.utils.httpobj import urlparse_cached

from logging import getLogger
from datetime import timedelta, datetime

import lxml.etree


logger = getLogger(__name__)


def strip_archive_prefix(link: str) -> str:
    try:
        if link.startswith("/web/"):
            return link.split('/', maxsplit=3)[3]
        if link.startswith("//web/"):
            return link.split('/', maxsplit=4)[4]
        if link.startswith("https://web.archive.org/web/"):
            return link.split('/', maxsplit=5)[5]
    except IndexError:
        pass
    return link


class Wayback:
    """
    Convert requests for normal HTTPS webpages to fetch from Wayback Machine's web archive.
    """

    def __init__(self, waybacked_domains: set[str], acceptible_age: timedelta):
        self.waybacked_domains: set[str] = waybacked_domains
        self.acceptible_age: timedelta = acceptible_age

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        domains: list[str] = crawler.settings.getlist("WAYBACK_DOMAINS")
        if not domains:
            raise NotConfigured("WAYBACK_DOMAINS setting must be a list of domains")
        acceptible_age: timedelta = timedelta(days=crawler.settings.get("WAYBACK_ACCEPTED_AGE_DAYS", default=1))
        return cls(waybacked_domains = set(domains), acceptible_age=acceptible_age)

    def process_request(self, request: Request) -> Request | Response | None:
        parsed = urlparse_cached(request)
        if parsed.hostname not in self.waybacked_domains:
            return None
        if parsed.hostname == 'web.archive.org' or request.meta.get('wayback_request'):
            return None

        try:
            cdx_api = WaybackMachineAvailabilityAPI(url=request.url, user_agent=str(request.headers['User-Agent']))
            meta = cdx_api.newest()

            if meta.json is None:
                raise CloseSpider("Failed to query wayback availability api")

            archive_url = meta.archive_url
            date_last_api_call = datetime.strptime(meta.json["timestamp"], "%Y%m%d%H%M%S")  # matching WaybackMachineAvailabilityAPI.timestamp()
            archived_ago: timedelta = date_last_api_call - meta.timestamp()

        except ArchiveNotInAvailabilityAPIResponse:
            archive_url = None
            archived_ago = timedelta(seconds=0)

        if archive_url is None or archived_ago >= self.acceptible_age:
            # need to update wayback item
            save_api = WaybackMachineSaveAPI(url=request.url, user_agent=str(request.headers['User-Agent']))
            logger.info("Saving new archive to wayback")
            archive_url = save_api.save()

        # Restart the request -- this function will receive the modified one and need to skip it.
        ret = request.replace(
            url=archive_url,
            dont_filter=True,
        )
        ret.meta['wayback_request'] = True
        ret.meta['wayback_original_url'] = request.url
        return ret

    def process_response(self, request: Request, response: Response) -> Response:
        if request.meta.get('wayback_request'):
            root_selector = response.xpath('.')[0]
            html_element = root_selector.root

            html_element.rewrite_links(strip_archive_prefix)

            rendered_fixed_html: str = lxml.etree.tostring(html_element).decode()

            return response.replace(
                url=strip_archive_prefix(response.url),
                body=rendered_fixed_html,
            )

        return response
