# How does a scrapy.Response handle html entities?

from scrapy.http import HtmlResponse


def test_response_nbsp_entity_assumption() -> None:
    response = HtmlResponse(
        url = 'https://example.com',
        status=200,
        body = b'<html><body><p>math 3 &lt; 5</p><div>spaces&nbsp;inline</div><time datetime="2020 &gt;&nbsp;" /></body></html>'
    )

    # extracting an element does not decode entities
    assert response.css("p").extract_first(default="") == "<p>math 3 &lt; 5</p>"
    assert response.css("p").get(default="") == "<p>math 3 &lt; 5</p>"

    # &lt; gets decoded to <
    assert response.css("p::text").extract_first(default="") == 'math 3 < 5'
    assert response.css("p::text").get(default="") == 'math 3 < 5'

    # &nbsp; gets decoded to \xa0 - text processors need to handle it
    assert response.css("div::text").extract_first(default="") == 'spaces\xa0inline'
    assert response.css("div::text").get(default="") == 'spaces\xa0inline'

    # non-breaking spaces are stripped by str.strip()
    assert "\xa0".strip() == ""

    # attribues are decoded too
    assert response.css("time").attrib['datetime'] == '2020 >\xa0'
