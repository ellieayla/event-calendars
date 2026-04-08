# See documentation in:
# https://docs.scrapy.org/en/latest/topics/download-handlers.html#writing-your-own-download-handler

from logging import getLogger
from typing import Self
from urllib.parse import ParseResult, urlunparse

from scrapy import Request
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.http import Response
from scrapy.utils.httpobj import urlparse_cached

logger = getLogger(__name__)


class CloudflareWorker:
    """
    Convert requests for normal HTTPS webpages
    on some domains to fetch via a Cloudflare Worker.
    """

    def __init__(self, domains: set[str], worker_domain: str):
        self.domains: set[str] = domains
        self.worker_domain: str = worker_domain
        self.logger = getLogger(__name__).getChild(f"CloudflareWorker({worker_domain})")

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        domains: list[str] = crawler.settings.getlist("CLOUDFLARE_WORKER_DOMAINS", default=[])
        if not domains:
            raise NotConfigured("CLOUDFLARE_WORKER_DOMAINS setting must be a list of domains")

        worker_domain: str = crawler.settings.get("CLOUDFLARE_WORKER_DOMAIN")
        if not worker_domain:
            raise NotConfigured("CLOUDFLARE_WORKER_DOMAIN must be a FQDN of a worker")

        if any(_ in worker_domain for _ in domains):
            raise NotConfigured("CLOUDFLARE_WORKER_DOMAINS must not be in CLOUDFLARE_WORKER_DOMAIN")

        return cls(domains=set(domains), worker_domain=worker_domain)

    def process_request(self, request: Request) -> Request | Response | None:
        parsed = urlparse_cached(request)

        if parsed.hostname == self.worker_domain:
            return None
        if parsed.hostname not in self.domains:
            return None

        new_components = ParseResult(
            scheme="https",
            netloc=self.worker_domain,
            path=f"/{parsed.hostname}{parsed.path}",
            params=parsed.params,
            query=parsed.query,
            fragment="",
        )

        new_url: str = urlunparse(new_components)

        self.logger.info(f"Rewriting {request.url} to {new_url}")

        # Restart the request -- this function will receive the modified one and need to skip it.
        ret = request.replace(
            url=new_url,
            dont_filter=True,
        )
        ret.meta["cloudflare_worker_original_url"] = request.url
        return ret

    def process_response(self, request: Request, response: Response) -> Response:
        if request.meta.get("cloudflare_worker_original_url"):
            return response.replace(
                url=request.meta.get("cloudflare_worker_original_url"),
                body=response.body,
            )

        return response
