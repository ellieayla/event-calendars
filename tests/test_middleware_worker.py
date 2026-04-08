import pytest
from scrapy.crawler import Crawler
from scrapy.exceptions import NotConfigured
from scrapy.http import HtmlResponse, Request

from event_calendars.middleware_worker import CloudflareWorker
from event_calendars.spiders.httpbin import HttpBinSpider


def test_load_from_crawler() -> None:
    crawler = Crawler(
        spidercls=HttpBinSpider,
        settings={"CLOUDFLARE_WORKER_DOMAINS": ["example.com"], "CLOUDFLARE_WORKER_DOMAIN": ["localhost"]},
    )
    CloudflareWorker.from_crawler(crawler=crawler)


def test_missing_domains_list() -> None:
    crawler = Crawler(
        spidercls=HttpBinSpider,
        settings={"CLOUDFLARE_WORKER_DOMAINS": []},
    )

    with pytest.raises(NotConfigured):
        CloudflareWorker.from_crawler(crawler=crawler)


def test_missing_worker_domain() -> None:
    crawler = Crawler(
        spidercls=HttpBinSpider,
        settings={"CLOUDFLARE_WORKER_DOMAINS": ["localhost"]},
    )

    with pytest.raises(NotConfigured):
        CloudflareWorker.from_crawler(crawler=crawler)


def test_conflicting_worker_domain() -> None:
    crawler = Crawler(
        spidercls=HttpBinSpider,
        settings={"CLOUDFLARE_WORKER_DOMAINS": ["localhost"], "CLOUDFLARE_WORKER_DOMAIN": "localhost"},
    )

    with pytest.raises(NotConfigured):
        CloudflareWorker.from_crawler(crawler=crawler)


def test_rewrite_request() -> None:
    mw = CloudflareWorker(domains=set(["example.com"]), worker_domain="localhost")

    request = Request(url="https://example.com/cdoyr")

    second_request = mw.process_request(request)

    assert isinstance(second_request, Request)
    assert second_request.url == "https://localhost/example.com/cdoyr"


def test_rewrite_response() -> None:
    mw = CloudflareWorker(domains=set(["example.com"]), worker_domain="localhost")

    request = Request(url="https://example.com/cdoyr")

    second_request = mw.process_request(request)

    assert isinstance(second_request, Request)
    assert second_request.url == "https://localhost/example.com/cdoyr"

    response = HtmlResponse(
        url=second_request.url,
        status=200,
        headers={"content-type": "text/html"},
        body="whatever",
        encoding="utf-8",
    )

    second_response = mw.process_response(second_request, response)

    assert second_response.url == request.url


def test_unmodified_response() -> None:
    mw = CloudflareWorker(domains=set(["example.net"]), worker_domain="localhost")

    request = Request(url="https://example.com/cdoyr")

    second_request = mw.process_request(request)

    assert second_request is None

    response = HtmlResponse(
        url=request.url,
        status=200,
        headers={"content-type": "text/html"},
        body="whatever",
        encoding="utf-8",
    )

    second_response = mw.process_response(request, response)

    assert second_response.url == request.url



def test_refuse_to_handle_own_domain() -> None:
    mw = CloudflareWorker(domains=set(["example.com"]), worker_domain="localhost")

    request = Request(url="https://localhost/")

    second_request = mw.process_request(request)

    assert second_request is None
