from pathlib import Path

import pytest
from scrapy import FormRequest, Request
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, TextResponse

from event_calendars.items import BookableEvent
from event_calendars.spiders.burlington_pools import BurlingtonPools

FIXTURE_DIR = Path(__file__).parent.parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "burlington-perfectmind-booking-pages-v2_get_request_verification_token.html")
def test_get_request_verification_token(datafiles: Path) -> None:
    EXPECTED_TOKEN = "x_Expected-Request-Verification-Token_x"  # just a random nonce, not a secret

    html_text: bytes = (datafiles / "burlington-perfectmind-booking-pages-v2_get_request_verification_token.html").read_bytes()

    assert b"__RequestVerificationToken" in html_text
    spider = BurlingtonPools()
    response = HtmlResponse(
        url='',
        status=200,
        body=html_text,
    )
    assert EXPECTED_TOKEN in response.text

    result = spider.parse(response)
    assert isinstance(result, FormRequest)
    print(result, result.body, result.callback, result.cb_kwargs)

    assert result.method == "POST"
    assert result.callback == spider.parse_classes_v2_json
    assert EXPECTED_TOKEN in str(result.body)
    assert result.cb_kwargs["verification_token"] == EXPECTED_TOKEN


@pytest.mark.datafiles(FIXTURE_DIR / "burlington-perfectmind-booking-pages-v2_get_request_verification_token.html")
def test_exception_on_mising_verification_token(datafiles: Path) -> None:
    EXPECTED_TOKEN = "x_Expected-Request-Verification-Token_x"  # just a random nonce, not a secret

    html_text: bytes = (datafiles / "burlington-perfectmind-booking-pages-v2_get_request_verification_token.html").read_bytes()
    assert b"__RequestVerificationToken" in html_text

    html_text = html_text.replace(b"__RequestVerificationToken", b"Trashed__RequestVerificationToken")

    spider = BurlingtonPools()
    response = HtmlResponse(
        url='',
        status=200,
        body=html_text,
    )
    assert EXPECTED_TOKEN in response.text

    with pytest.raises(CloseSpider) as e:
        _result = spider.parse(response)
        assert "Failed to extract __RequestVerificationToken from form" == e.value.reason


@pytest.mark.datafiles(FIXTURE_DIR / "burlington-perfectmind-booking-pages-v2-classes-v2-20260329.json")
def test_parse_events_list_page(datafiles: Path) -> None:
    assert datafiles.is_dir()

    json_text: bytes = (datafiles / "burlington-perfectmind-booking-pages-v2-classes-v2-20260329.json").read_bytes()
    assert json_text.startswith(b'{"classes":[')

    spider = BurlingtonPools()

    response = TextResponse(
        url='',
        status=200,
        body=json_text
    )

    results = list(spider.parse_classes_v2_json(response, verification_token=""))

    assert len(results) == 79

    assert isinstance(results[0], BookableEvent)
    assert results[0].summary == "Lap Swim"

    # the yielded sequence ends with a Request for the next page of items citing the same callback
    assert isinstance(results[-1], Request)
    assert "POST" == results[-1].method
    assert spider.parse_classes_v2_json == results[-1].callback
