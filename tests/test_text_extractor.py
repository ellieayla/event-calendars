from pathlib import Path
from textwrap import dedent

import pytest
from lxml.html import HtmlElement, fromstring
from scrapy.http import HtmlResponse

from event_calendars.utils import extract_text_visitor, readable_text_content

FIXTURE_DIR = Path(__file__).parent.parent.resolve() / "test_data"


@pytest.mark.datafiles(FIXTURE_DIR / "cycleto.ca-event-cdoyr-2026.html")
def test_extractor_on_cycleto_event_html(datafiles: Path) -> None:
    """The extrator was originally designed to read descriptions from CycleTO event webpages."""

    html: bytes = (datafiles / "cycleto.ca-event-cdoyr-2026.html").read_bytes()

    response = HtmlResponse(url="unused", status=200, body=html)

    root_node: HtmlElement = response.css("main div.text-content.inner-block")[0].root
    assert isinstance(root_node, HtmlElement)

    undesirable_strings = (
        "Drive)Ride",  # newlines missing
        "2026Time",
        "Click here to reserve",  # missing url
    )

    desirable_strings = (
        "Drive)\nRide",  # newlines before new lines
        "2026\nTime",  #
        "Click https://",  # urls
        "Coldest Day of the Year Ride 2026!\n\nThe Coldest Day",  # paragraph breaks
        "\n\n",
    )

    # Spot checks of the undesirable results of node.text_content() are easier to diagnose than diff against the big string
    bad_content = root_node.text_content()
    for _ in undesirable_strings:
        assert _ in bad_content
    for _ in desirable_strings:
        assert _ not in bad_content

    # Note that there are some non-breaking space characters \xa0 and extra whitespace embedded in the bad_content
    assert bad_content == "                       \n" + dedent(
        """\
        Coldest Day of the Year Ride 2026!
        The Coldest Day of the Year Ride is an annual ride organized by Cycle Toronto in partnership with the City of Toronto and Bike Share Toronto, to celebrate and support winter cycling for Bike Winter.\xa0
        Join us in this all-ages-and-abilities annual celebration of winter cycling. The ride starts and ends at Sugar Beach Park where we'll finish up with some hot chocolate and light snacks!
        Date: Saturday, February 28, 2026Time: 10:00 amLocation:\xa0Sugar Beach Park (11 Dockside Drive)Ride Distance: ~10kmRoute: https://ridewithgps.com/routes/54023563
        Bike Share Toronto is offering free bike share reservations while supplies last. Click here to reserve a complimentary Bike Share bike for the ride.\xa0  """
    )

    # Better output
    good_content = readable_text_content(root_node)

    # spot checks are easier to diagnose
    for _ in undesirable_strings:
        assert _ not in good_content

    for _ in desirable_strings:
        assert _ in good_content

    assert good_content == dedent(
        """\
        Coldest Day of the Year Ride 2026!

        The Coldest Day of the Year Ride is an annual ride organized by Cycle Toronto in partnership with the City of Toronto and Bike Share Toronto, to celebrate and support winter cycling for Bike Winter.

        Join us in this all-ages-and-abilities annual celebration of winter cycling. The ride starts and ends at Sugar Beach Park where we'll finish up with some hot chocolate and light snacks!

        Date: Saturday, February 28, 2026
        Time: 10:00 am
        Location: (https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=2261) Sugar Beach Park (11 Dockside Drive)
        Ride Distance: ~10km
        Route: https://ridewithgps.com/routes/54023563

        Bike Share Toronto is offering free bike share reservations while supplies last. Click https://docs.google.com/forms/d/e/1FAIpQLSc5_WzgwtXdc-BJ6WtyOKNmbPZwcEdu3rpUT5e2v44Xo7nfrw/viewform?usp=dialog to reserve a complimentary Bike Share bike for the ride."""
    )


def test_visitor_simple() -> None:
    html = fromstring("""<h1>some heading</h1><p>paragraph</p>""")

    nodes = list(extract_text_visitor(html, 0))
    print(html)
    print(nodes)
    assert nodes == [
        "\n\n",
        "some heading",
        "\n\n",
        "paragraph",
        "\n\n",
        "\n\n",
    ]

    pretty = readable_text_content(html)
    assert pretty == """some heading\n\nparagraph"""


def test_interstitial_whitespace() -> None:
    html = fromstring(
        """
        <ul>
        <li>
        inside

        </li>


        <li>

                second
        </li>
        </ul>
        """
    )
    pretty = readable_text_content(html)
    assert pretty == """* inside\n* second"""


def test_extract_text() -> None:
    # example_text = response.css("main div.text-content.inner-block").get()
    example_text = '<div class=" text-content inner-block spacing-none  inline-size-text   ">                       <p class="m_-5919225877674904153MsoNoSpacing"><img loading="lazy" decoding="async" src="https://cdn.nationbuilderthemes.ca/cycletoronto/tr:q-85,c-at_max,w-1680/pages/10318/attachments/original/1769800088/CDOTYR_2026_email_banner_%281%29.png?1769800088" alt="" width="600" height="300"></p>\n<p class="m_-5919225877674904153MsoNoSpacing"><strong><span>Coldest Day of the Year Ride 2026!</span></strong></p>\n<p class="m_-5919225877674904153MsoNoSpacing"><span><span>The Coldest Day of the Year Ride is an annual ride organized by Cycle Toronto in partnership with the City of Toronto and Bike Share Toronto, to celebrate and support winter cycling for Bike Winter.\xa0</span></span></p>\n<p class="m_-5919225877674904153MsoNoSpacing"><span>Join us in this all-ages-and-abilities annual celebration of winter cycling. The ride starts and ends at Sugar Beach Park where we\'ll finish up with some hot chocolate and light snacks!</span><strong><span><br></span></strong></p>\n<p class="m_-5919225877674904153MsoNoSpacing"><strong><span>Date:</span></strong><span> Saturday, February 28, 2026<br></span><strong>Time:</strong> Meet for 10:00 am, roll out around 10:30 am<br><strong>Location:</strong>\xa0<a rel="noopener" href="https://www.toronto.ca/explore-enjoy/parks-recreation/places-spaces/parks-and-recreation-facilities/location/?id=2261" target="_blank">Sugar Beach Park (11 Dockside Drive)</a><br><strong>Ride Distance: ~</strong>10km<br><strong>Route: </strong>[coming soon]</p>\n<div>Bike Share Toronto is offering free bike share reservations while supplies last. Click <a href="https://docs.google.com/forms/d/e/1FAIpQLSc5_WzgwtXdc-BJ6WtyOKNmbPZwcEdu3rpUT5e2v44Xo7nfrw/viewform?usp=dialog">here</a> to reserve a complimentary Bike Share bike for the ride.\xa0</div>  </div>'
    root = fromstring(example_text)
    assert isinstance(root, HtmlElement)

    produced = readable_text_content(root)

    for line in produced.splitlines():
        leader = line.split(":", maxsplit=1)[0]
        if ":" in line and len(leader) < 10:
            assert leader in ("Date", "Time", "Location", "Ride Distance", "Route")

    assert produced.startswith("Coldest Day")
    assert produced.endswith("for the ride.")


def test_extract_text_list() -> None:
    example_text = """<div>preceeding<ul><li>a</li><li><strong>b:</strong>more</li></ul>trailing</div>"""
    root = fromstring(example_text)
    assert isinstance(root, HtmlElement)

    produced = readable_text_content(root)

    assert produced == "preceeding\n\n* a\n* b:more\n\ntrailing"


def test_nested_lists() -> None:
    html = """<div><ul><li>a</li><li><ol><li>1</li><li>2</li></ol></li><li>b</li></ul></div>"""
    root = fromstring(html)
    assert isinstance(root, HtmlElement)

    produced = readable_text_content(root)

    assert produced == """* a\n\n* * 1\n* * 2\n\n* b"""


def test_only_root_node() -> None:
    html = "<div />"
    root = fromstring(html)
    assert isinstance(root, HtmlElement)

    produced = readable_text_content(root)

    assert produced == ""


def test_inline_nbsp() -> None:
    html = "<p>1\xa02</p>"
    root = fromstring(html)
    produced = readable_text_content(root)
    assert produced == "1 2"


def test_list_of_paragraph_nodes_wrapped_in_div_by_lxml_html_fromstring() -> None:
    html = "<p>1</p><p>2</p>"
    root = fromstring(html)
    assert isinstance(root, HtmlElement)
    assert root.tag == "div"

    produced = readable_text_content(root)

    assert produced == "1\n\n2"
