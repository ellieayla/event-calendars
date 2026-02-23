
from typing import Iterable

from lxml.html import HtmlElement
import re

from scrapy.selector import SelectorList, Selector
from parsel import Selector as ParselSelector
from w3lib.html import remove_tags


def extract_text_visitor(node: HtmlElement | str, indent: int = 0) -> Iterable[str]:
    """
    Use the Visitor Pattern to traverse the tree starting from 'node',
    yielding plain text.
    """

    if isinstance(node, str):
        if node == "":
            return
        yield node
        return

    assert isinstance(node, HtmlElement)

    if node.tag in ('img:', ):
        print("dropped image")
        return  # drop

    if node.tag in ('p', 'div', 'ol', 'ul'):
        yield "\n\n"  # add double-newlines around block elements
    if node.tag in ('br', 'li'):
        yield "\n"
    if node.tag in ('li', ):
        if not all([isinstance(child, HtmlElement) and child.tag in ('ol', 'ul') for child in node.xpath("child::node()")]):
            yield "* " * (indent+1)
        indent += 1

    if node.tag in ('a'):
        if node.text == "here":
            yield node.attrib.get("href")
            return  # drop content
        else:
            yield f' ({node.attrib.get("href")}) '

    for child in node.xpath("child::node()"):
        yield from extract_text_visitor(child, indent=indent)

    if node.tag in ('p', 'div', 'ol', 'ul'):
        yield "\n\n"  # add double-newlines around block elements


def readable_text_content(node: HtmlElement) -> str:
    """
    Replacement for HtmlElement.text_content() that honours whitespace.
    node = response.css("main div.text-content.inner-block")[0].root
    """
    text = "".join(extract_text_visitor(node, 0))

    # segments of text produced by the visitor might contain ajacent newlines,
    # which should be collapsed to produce readable text
    # like (..., "first\n\n", "\n\nsecond", ...) -> "first\n\nsecond"

    text = text.replace("\xa0", " ")  # non-breaking space
    text = re.sub("[ ]+", " ", text)  # combine runs of adjacent spaces
    text = re.sub("\n\n+", "\n\n", text)  # drop 3+ newlines back to 2
    text = re.sub(" *(\n+) *", "\\1", text)  # drop spaes alongside newlines
    text = text.strip()  # drop leading and trailing whitespace
    return text


def remove_node(nodes_to_remove: list[Selector | ParselSelector] | SelectorList) -> None:
    for node_to_remove in nodes_to_remove:
        node_to_remove.root.getparent().remove(node_to_remove.root)


def remove_empty_nodes(selector_list: SelectorList) -> None:
    remove_node([_ for _ in selector_list if not remove_tags(_.extract()).strip()])
