from __future__ import annotations

import re
from enum import Enum
from typing import Iterable, List, Optional

from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

IGNORED_EMPHASIS_TAGS = ["var", "i", "b", "a"]
PREFIX_SYMBOL_TAGS = {"sup": "^", "sub": "_"}

# https://html.spec.whatwg.org/multipage/dom.html#content-models


class Mode(Enum):
    BLOCK = 1
    INLINE = 2
    CELL = 3


def htmlToDocstring(text: str) -> str:
    soup = BeautifulSoup(text, "html.parser")
    return "\n\n".join(
        block
        for child in soup.children
        if (block := format_element(child, Mode.BLOCK)) is not None
    )


def format_elements(elements: Iterable[PageElement], mode: Mode) -> List[str]:
    return [s for elt in elements if (s := format_element(elt, mode)) is not None]


def format_element(element: PageElement, mode: Mode) -> Optional[str]:
    if isinstance(element, Tag):
        return format_tag(element, mode)
    elif isinstance(element, NavigableString):
        return format_string(element, mode)
    else:
        raise Exception(f"Unexpected element: {element}")


def format_tag(tag: Tag, mode: Mode) -> str:
    if tag.name in IGNORED_EMPHASIS_TAGS:
        return "".join(format_elements(tag.children, mode))
    if tag.name in PREFIX_SYMBOL_TAGS:
        return PREFIX_SYMBOL_TAGS[tag.name] + "".join(
            format_elements(tag.children, mode)
        )
    if tag.name == "p":
        return "".join(format_elements(tag.children, Mode.INLINE))
    elif tag.name == "div":
        sep = "\n" if mode == Mode.BLOCK else ""
        return sep.join(format_elements(tag.children, mode))
    elif tag.name == "blockquote":
        text = "".join(format_elements(tag.children, Mode.INLINE))
        return indent_block(text, 4, False)
    elif tag.name == "ol":
        items = format_elements(tag.children, mode)
        return "\n".join(
            f"{i+1}. {indent_block(item, 3, True)}" for (i, item) in enumerate(items)
        )
    elif tag.name == "ul":
        items = format_elements(tag.children, mode)
        return "\n".join(f"- {indent_block(item, 2, True)}" for item in items)
    elif tag.name == "li":
        return "".join(format_elements(tag.children, Mode.INLINE))
    elif tag.name == "br":
        return "<br>" if mode == Mode.CELL else "\n"
    elif tag.name == "table":
        return "\n".join(format_elements(tag.children, mode))
    elif tag.name == "tr":
        # TODO space cells out nicely
        return "    ".join(format_elements(tag.children, mode))
    elif tag.name == "td":
        return "".join(format_elements(tag.children, Mode.CELL))
    else:
        attrs = ",".join(
            f"{key}={''.join(values)}" for (key, values) in tag.attrs.items()
        )
        contents = "".join(format_elements(tag.children, mode))
        return f"<{tag.name} {attrs}>{contents}</{tag.name}>"


def format_string(ns: NavigableString, mode: Mode) -> Optional[str]:
    # If we're in a block context, discard leading and trailing space,
    # and call it a day
    if mode == Mode.BLOCK:
        return str(ns).strip() or None
    elif mode == Mode.INLINE:
        # https://www.w3.org/TR/css-text-3/#white-space-rules
        text = str(ns).replace("\t", " ")
        text = re.sub(" *\n *", " ", text)
        text = re.sub(" +", " ", text)
        # Okay, here's a kludge. We want to preserve spaces most of the time,
        # (e.g., `1<sup>st</sup> thing` should keep the space).
        # But `1<br />\n2` should drop the newline
        prev = ns.previous_sibling
        if isinstance(prev, Tag) and prev.name == "br":
            text = text.lstrip()
        next = ns.next_sibling
        if isinstance(next, Tag) and next.name == "br":
            text = text.rstrip()

        return text or None
    elif mode == Mode.CELL:
        return str(ns).strip().replace("\n", "<br>")

    raise AssertionError()


def indent_block(s: str, indent: int, skip_first: bool) -> str:
    return "\n".join(
        line if skip_first and i == 0 else " " * indent + line
        for (i, line) in enumerate(s.splitlines())
    )
