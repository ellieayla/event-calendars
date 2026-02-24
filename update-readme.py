#!/usr/bin/env python

import sys
from argparse import ArgumentParser, Namespace
from collections.abc import Sequence
from glob import glob
from pathlib import Path
from typing import NamedTuple

from marko import Markdown
from marko.block import Document, Heading, List, ListItem
from marko.ext.gfm import GFM
from marko.inline import RawText
from marko.md_renderer import MarkdownRenderer


class MarkdownLink(NamedTuple):
    label: str
    url: str

    def __str__(self) -> str:
        """Very simple, no escaping logic"""
        return f"[{self.label}]({self.url})"


class Arguments(Namespace):
    readme: Path
    write: Path
    matching: str
    url_prefix: str
    empty_is_ok: bool


def replace_listitems(md: Document, replacement_listitems: Sequence[ListItem]) -> None:
    # find the Feeds heading
    inside_feeds_heading_section = False

    for c in md.children:
        if isinstance(c, Heading):
            inside_feeds_heading_section = False

        if (
            isinstance(c, Heading)
            and c.children
            and isinstance(c.children[0], RawText)
            and c.children[0].children == "Feeds"
        ):
            print(f"Found Feeds heading at {c=} / {c.children[0]=}")
            inside_feeds_heading_section = True

        if inside_feeds_heading_section and isinstance(c, List):
            # replace all the list children
            c.children = replacement_listitems

            # TODO: It should be possible to create ListItem objects without parsing a document fragment
            """
            list_info = c.ParseInfo(c.bullet, c.ordered, c.start)
            list_item_info = ListItem.ParseInfo(indent=1, bullet="*", mid=1)  # desired list item style

            i = ListItem(info=list_item_info)
            i.children = []

            print(f"created {i=}")
            p = Paragraph("aaaaa")
            print(p)
            i.children.append(p)

            c.children.append(i)
            #for link in replace_links:
            #    i = ListItem(info=list_item_info)
            #    print(i)
            """

        print(f"infeed={inside_feeds_heading_section}", c)


def process_document(original: str, replacement_document_fragment: str) -> str:
    md_fragment = Markdown(extensions=[GFM], renderer=MarkdownRenderer)
    parsed_fragment = md_fragment.parse(replacement_document_fragment)
    if not isinstance(parsed_fragment.children[0], List):
        raise ValueError(
            f"Unparsable replacement document fragment: {replacement_document_fragment}"
        )
    replacement_listitems: Sequence[ListItem] = [
        el for el in parsed_fragment.children[0].children if isinstance(el, ListItem)
    ]

    md = Markdown(extensions=[GFM], renderer=MarkdownRenderer)
    parsed = md.parse(original)
    replace_listitems(parsed, replacement_listitems)
    return md.render(parsed)


def main() -> int:
    p = ArgumentParser()

    p.add_argument(
        "--readme",
        metavar="README.MD",
        type=Path,
        default="README.md",
        help="Read template markdown file (default %(default)s)",
    )
    p.add_argument(
        "--write",
        metavar="README.MD",
        type=Path,
        default="/dev/stdout",
        help="Write results to file or stdout (default %(default)s)",
    )
    p.add_argument(
        "--matching",
        metavar="**.ical",
        type=str,
        default="out/*.ical",
        help="Glob pattern of files to include, (default %(default)s)",
    )
    p.add_argument(
        "--url-prefix",
        metavar="URL",
        type=str,
        default="https://github.com/ellieayla/event-calendars/raw/refs/heads/main/",
        help="Fully qualified url to prepend on all filenames (default %(default)s)",
    )
    p.add_argument(
        "--empty-is-ok",
        action="store_true",
        help="If no files match the glob, write an empty list to markdown file. (default: exit with error)",
    )

    a = p.parse_args(namespace=Arguments())

    ical_files = glob(a.matching, recursive=True)
    if not a.empty_is_ok and len(ical_files) == 0:
        p.error("Did not find any matching files.")

    print(f"Found ical files: {ical_files}")

    new_link_document_fragment = "\n".join(
        [
            "* "
            + str(
                MarkdownLink(
                    label=Path(filename).name,
                    url=a.url_prefix + filename,
                )
            )
            for filename in ical_files
        ]
    )

    original_markdown_document = a.readme.read_text()

    new_document = process_document(
        original_markdown_document, new_link_document_fragment
    )

    if a.write is sys.stdout:
        sys.stdout.write(new_document)
    else:
        a.write.write_text(new_document)

    return 0


### inline self-tests


def test_render_markdown_link() -> None:
    link = MarkdownLink("label", "https://example.com/")
    assert "[label](https://example.com/)" == str(link)


def test_process_markdown_text() -> None:
    document = f"""\
leading text
# Something else
* ignored
## Feeds
* {str(MarkdownLink("label", "https://example.com/"))}
* {str(MarkdownLink("labelwww", "https://www.example.com/"))}
footer
"""

    list_fragment = f"""* {str(MarkdownLink("LABEL", "https://example.com/"))}"""

    result = process_document(document, list_fragment)
    assert "label" not in result
    assert "LABEL" in result


if __name__ == "__main__":
    raise SystemExit(main())
