
from scrapy.http import HtmlResponse, Request

from event_calendars.middleware import Wayback
from datetime import timedelta


def test_replace_body_links() -> None:
    body_template = """<html><body><div class="calendar-list"><a href="%s">link</a></div></body></html>"""
    stored_url = "/web/20260215055933/https://www.example.com/cdoyr"
    desired_url = "https://www.example.com/cdoyr"

    response = HtmlResponse(
        url = "https://web.archive.org/web/123/http://original.one.example.com/document",
        status=200,
        headers={"content-type": "text/html"},
        body=body_template % stored_url,
        encoding='utf-8',
    )

    download_middleware = Wayback(waybacked_domains=set(), acceptible_age=timedelta(seconds=0))

    second_response = download_middleware.process_response(Request(url=response.url, meta={"wayback_request": True}), response)

    desired_body = body_template % desired_url
    assert second_response.body.decode() == desired_body

    assert second_response.url == 'http://original.one.example.com/document'
    assert response.css(".calendar-list a::attr(href)").get() == desired_url
