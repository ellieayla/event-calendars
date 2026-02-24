
import re
from collections.abc import Iterator

from lxml.html import HtmlElement
from parsel import Selector as ParselSelector
from scrapy.selector import Selector, SelectorList
from w3lib.html import remove_tags


def extract_text_visitor(node: HtmlElement | str, indent: int = 0) -> Iterator[str]:
    """
    Use the Visitor Pattern to traverse the tree starting from 'node',
    yielding plain text.
    """

    if isinstance(node, str):
        if node == "":
            return
        #if node.strip() == "":
            #raise ValueError("weird node", node)
        #    return
        if node.strip() == "":
            yield ""
        yield node.replace("\n", " ")

        #yield node
        return

    assert isinstance(node, HtmlElement)

    if node.tag in ('img', ):
        return  # drop images

    if node.tag in ('p', 'div', 'ol', 'ul'):
        yield "\n\n"  # add double-newlines around block elements
    if node.tag in ('br', ):
        yield "\n"
    if node.tag in ('li', ):
        if not all([isinstance(child, HtmlElement) and child.tag in ('ol', 'ul') for child in node.xpath("child::node()")]):
            yield "\n"
            yield "* " * (indent+1)
        indent += 1

    if node.tag in ('a'):
        if node.text == "here":
            yield node.attrib.get("href")
            return  # drop content
        elif node.text.strip() == node.attrib.get("href"):
            yield node.attrib.get("href")
            return  # drop content
        else:
            # prepend url as (https://...)
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
