import dataclasses
from typing import Literal, Optional

from bs4 import BeautifulSoup, NavigableString, PageElement, Tag


@dataclasses.dataclass
class Formatter:
    """
    Formats HTML problem descriptions into plain text
    """

    indent: int = 0
    buffer: str = ""
    list_type: Optional[Literal["-"]] = None

    def handle_tag(self, tag: Tag) -> None:
        if tag.name == "p":
            self.start_block()
        elif tag.name == "blockquote":
            self.indent += 4
            self.start_block()
        elif tag.name == "div":
            self.start_block()
        elif tag.name == "var":
            pass
        elif tag.name == "i":
            pass
        elif tag.name == "sup":
            # TODO fractions are sometimes written as ^a/_b
            self.buffer += "^"
        elif tag.name == "sub":
            self.buffer += "_"
        elif tag.name == "br":
            self.end_block()
            self.start_block()
        elif tag.name == "ul":
            self.list_type = "-"
        elif tag.name == "li":
            self.start_block()
            if self.list_type is not None:
                self.buffer += self.list_type + " "
        else:
            self.buffer += f"<{tag.name}>"

    def handle_untag(self, tag: Tag) -> None:
        if tag.name == "p":
            self.end_block()
        elif tag.name == "blockquote":
            self.indent -= 4
            self.end_block()
        elif tag.name == "div":
            self.end_block()
        elif tag.name == "var":
            pass
        elif tag.name == "i":
            pass
        elif tag.name == "sup":
            pass
        elif tag.name == "sub":
            pass
        elif tag.name == "br":
            pass
        elif tag.name == "ul":
            pass
        elif tag.name == "li":
            self.end_block()
        else:
            self.buffer += f"</{tag.name}>"

    def start_block(self) -> None:
        self.buffer += " " * self.indent

    def end_block(self) -> None:
        self.buffer = self.buffer.strip() + "\n"

    def consume(self, element: PageElement) -> None:
        if isinstance(element, BeautifulSoup):
            for ch in element.children:
                self.consume(ch)
        elif isinstance(element, Tag):
            self.handle_tag(element)
            for ch in element.children:
                self.consume(ch)
            self.handle_untag(element)
        elif isinstance(element, NavigableString):
            self.buffer += str(element.lstrip("\n"))
        else:
            raise Exception(f"UNRECOGNIZED ELEMENT: {element}")

    def output(self) -> str:
        return self.buffer.strip()
