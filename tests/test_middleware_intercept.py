from pathlib import Path

import pytest
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Request

from event_calendars.middleware_warn_cloudflare import DetectCloudflareIntercepted

FIXTURE_DIR = Path(__file__).parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "cloudflare-block-page.html")
def test_intercept(datafiles: Path) -> None:
    assert datafiles.is_dir()

    html_text: bytes = (datafiles / "cloudflare-block-page.html").read_bytes()
    assert html_text.startswith(b'<!')

    request = Request(url="https://example.com/")

    response = HtmlResponse(
        url=request.url,
        status=403,
        headers={"content-type": "text/html"},
        body=html_text,
        encoding="utf-8",
    )

    mw = DetectCloudflareIntercepted()

    with pytest.raises(CloseSpider):
        result = mw.process_response(request, response)

        print(f"{result=}")

def test_no_intercept() -> None:
    request = Request(url="https://example.com/")

    response = HtmlResponse(
        url=request.url,
        status=200,
        headers={"content-type": "text/html"},
        body=b'ok',
        encoding="utf-8",
    )

    mw = DetectCloudflareIntercepted()

    result = mw.process_response(request, response)

    assert result is response  # passed right through
