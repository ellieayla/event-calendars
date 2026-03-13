import logging
import re
from collections.abc import Iterator, Sequence
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import dateutil
from lxml.html import HtmlElement
from parsel import Selector as ParselSelector
from scrapy.selector import Selector, SelectorList
from w3lib.html import remove_tags


def extract_text_visitor(node: HtmlElement | str, indent: int = 0, skip_block_newlines: bool = False) -> Iterator[str]:
    """
    Use the Visitor Pattern to traverse the tree starting from 'node',
    yielding plain text.
    """

    p_in_li = False

    if isinstance(node, str):
        if node == "":
            return
        if node.strip() == "":
            yield ""
        yield node.replace("\n", " ")

        return

    assert isinstance(node, HtmlElement)

    if node.tag in ("img",):
        return  # drop images

    if node.tag in ("p", "div", "ol", "ul") and not skip_block_newlines:
        yield "\n\n"  # add double-newlines around block elements
    if node.tag in ("br",):
        yield "\n"
    if node.tag in ("li",):
        if (
            len(node.xpath("child::node()")) == 1
            and isinstance(node.xpath("child::node()")[0], HtmlElement)
            and node.xpath("child::node()")[0].tag in ("p", "div")
        ):
            p_in_li = True
        if not all([isinstance(child, HtmlElement) and child.tag in ("ol", "ul") for child in node.xpath("child::node()")]):
            yield "\n"
            yield "* " * (indent + 1)
        indent += 1

    if node.tag in ("a"):
        if node.text == "here":
            yield node.attrib.get("href")
            return  # drop content
        elif node.text is not None and node.text.strip() == node.attrib.get("href"):
            yield node.attrib.get("href")
            return  # drop content
        else:
            # prepend url as (https://...)
            yield f" ({node.attrib.get('href')}) "

    for child in node.xpath("child::node()"):
        yield from extract_text_visitor(child, indent=indent, skip_block_newlines=p_in_li)

    if node.tag in ("p", "div", "ol", "ul") and not skip_block_newlines:
        yield "\n\n"  # add double-newlines around block elements


def readable_text_content(node: HtmlElement) -> str:
    """
    Replacement for HtmlElement.text_content() that honours whitespace.
    node = response.css("main div.text-content.inner-block")[0].root
    """
    chunks = list(extract_text_visitor(node, 0))
    text = "".join(chunks)

    # segments of text produced by the visitor might contain ajacent newlines,
    # which should be collapsed to produce readable text
    # like (..., "first\n\n", "\n\nsecond", ...) -> "first\n\nsecond"

    text = text.replace("\xa0", " ")  # non-breaking space
    text = re.sub("[ ]+", " ", text)  # combine runs of adjacent spaces
    text = re.sub("\n +", "\n", text, re.MULTILINE)  # drop spaes alongside newlines
    text = re.sub(" +\n", "\n", text, re.MULTILINE)
    text = re.sub("\n\n+", "\n\n", text, re.MULTILINE)  # drop 3+ newlines back to 2
    text = text.strip()  # drop leading and trailing whitespace

    return text


def remove_node(nodes_to_remove: list[Selector | ParselSelector] | SelectorList) -> None:
    for node_to_remove in nodes_to_remove:
        node_to_remove.root.getparent().remove(node_to_remove.root)


def remove_empty_nodes(selector_list: SelectorList) -> None:
    remove_node([_ for _ in selector_list if not remove_tags(_.extract()).strip()])


def extract_dates_from_description(description: str, default_tzinfo: ZoneInfo) -> tuple[datetime, datetime | None]:
    start_date: date | None = None
    start_time: time = time(hour=0, minute=0, tzinfo=default_tzinfo)
    end_date: date | None = None
    end_time: time | None = None

    description = description.replace("\u2013", "-")  # fancy hyphen

    RE_COLON_ITEM = re.compile(r"(?P<key>\w{1,15}): *(?P<value>.*)")
    RE_URL = re.compile(r"\(https?://\w+?\)", re.IGNORECASE)

    RE_TIME_RANGE = re.compile(r"(?P<lead>.*) (?P<left>\d\d?(:\d\d)?) *(-|to) *(?P<right>\d\d?(:\d\d)?) (?P<trail>.*)")

    for possible_date in description.splitlines():
        if "today" in possible_date.lower():
            continue  # skip the donation request

        m = RE_TIME_RANGE.match(possible_date)
        if m:
            a_string = f"{m.group('lead')} {m.group('left')} {m.group('trail')}"
            b_string = f"{m.group('lead')} {m.group('right')} {m.group('trail')}"

            try:
                _start_datetime, _ = extract_dates_from_description(a_string, default_tzinfo=default_tzinfo)
                _end_datetime, _ = extract_dates_from_description(b_string, default_tzinfo=default_tzinfo)

                if _start_datetime >= _end_datetime:
                    _start_datetime = _start_datetime - timedelta(hours=12)
                return (_start_datetime, _end_datetime)
            except ValueError:
                pass  # that didn't work, carry on with detection

        m = RE_COLON_ITEM.match(possible_date)
        if m:
            match m.group("key").lower():
                case "date":
                    start_date = dateutil.parser.parse(m.group("value"))
                    logging.getLogger().debug(f"Found start date in description key: {possible_date=} {start_date=}")
                    continue
                case "time":
                    start_time = dateutil.parser.parse(m.group("value")).time().replace(tzinfo=default_tzinfo)
                    continue
                case _:
                    pass

        try:
            simple_description = RE_URL.sub("", possible_date)
            # print(f"{possible_date=} {simple_description=}")
            _start_datetime = dateutil.parser.parse(simple_description, fuzzy=True)
            start_date = _start_datetime.date()
            start_time = _start_datetime.time().replace(tzinfo=default_tzinfo)

            logging.getLogger().debug(f"Found start date in description body: {possible_date=} {start_date=}")
        except dateutil.parser.ParserError:
            pass

    if start_date is None:
        raise ValueError("Failed to find a start date in description")

    start_datetime: datetime = datetime.combine(start_date, start_time)
    end_datetime = None
    if end_time:
        if end_date:
            end_datetime = datetime.combine(end_date, end_time)
        else:
            end_datetime = datetime.combine(start_date, end_time)

    return (start_datetime, end_datetime)


def extract_dates_from_metadata(header_metadata_items: Sequence[str], default_tzinfo: ZoneInfo) -> tuple[datetime, datetime | None]:
    start_date: date | None = None
    start_time: time = time(hour=0, minute=0, tzinfo=default_tzinfo)
    end_date: date | None = None
    end_time: time | None = None

    for header_text in header_metadata_items:
        if " : " in header_text:
            header_text = header_text.replace(" : ", ":")

        try:
            (found_date_chunk, leftover_tokens) = dateutil.parser.parse(header_text, fuzzy_with_tokens=True)
            found_date_chunk = found_date_chunk.replace(tzinfo=default_tzinfo)
            simple_header_text = "".join(leftover_tokens).lower()
        except dateutil.parser.ParserError:
            continue

        logging.getLogger().debug(f"Found {found_date_chunk} in {header_text=}")
        if "time" in simple_header_text:
            if "end" in simple_header_text:
                end_time = found_date_chunk.time().replace(tzinfo=default_tzinfo)
            else:
                start_time = found_date_chunk.time().replace(tzinfo=default_tzinfo)
        else:
            if "end" in simple_header_text:
                end_date = found_date_chunk.date()
            else:
                start_date = found_date_chunk.date()

    if start_date is None:
        raise ValueError("Failed to find a start date in metadata")

    start_datetime = datetime.combine(start_date, start_time)

    if end_time:
        if end_date:
            end_datetime = datetime.combine(end_date, end_time)
        else:
            end_datetime = datetime.combine(start_date, end_time)
    elif end_date:
        end_datetime = datetime.combine(end_date, time(hour=0, minute=0, tzinfo=default_tzinfo))
    else:
        end_datetime = None

    return (start_datetime, end_datetime)


def extract_location_from_description(description: str) -> str | None:
    AT_RE = re.compile(r"(location| at ):? *(?P<place>[^\.]+)")
    for row in description.splitlines():
        # if row.lower().startswith(LOC_HEADER):
        #    return row[len(LOC_HEADER):].strip()

        m = AT_RE.search(row)
        if m:
            return m.group("place").strip()

    return None
