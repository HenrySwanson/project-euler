#!/usr/bin/env python

import dataclasses
import itertools
import os
from importlib import import_module
from time import perf_counter
from typing import Dict, List
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag

import click
import requests

TEMPLATE_FILE = "problem.py.template"
ANSWER_FILE = "answers.bin"

# ==== TODO LIST ====
# - maybe make scramble and unscramble depend on an un-checked-in file
#   that i can conjure from memory?
#   - nah, too much effort
# - include timing info per-problem?
# - tests
# - if i forget to save, how can i run a command to check that?
# - `next` command?
# - an interactive mode would be cool!
#  - open 25, create, run, run, ..., run, save
#  - would have to force a reload of all py files though...
# - i wonder if i can yank the problem descriptions right from the site?
# - run and check are pretty similar, it'd be nice to have them unified
#   - both run the solver, and the only difference is whether there's an answer already saved


def filename(n: int) -> str:
    return f"{n:04}"


# I put in some very basic fuckery here so that I'm not just writing a list of
# plaintext answers directly to GitHub.
# Is it unbreakable encryption? No. But if someone wants the answers from my repo
# they could just run the problem solvers anyways, so whatever.


def scramble(input: str) -> bytes:
    nonsense = itertools.cycle(range(256))
    return bytes(x ^ y for (x, y) in zip(input.encode(), nonsense))


def unscramble(input: bytes) -> str:
    nonsense = itertools.cycle(range(256))
    return bytes(x ^ y for (x, y) in zip(input, nonsense)).decode()


def parse_answer_file() -> Dict[int, int]:
    with open(ANSWER_FILE, "rb") as f:
        contents: bytes = f.read()

    if not contents:
        return {}

    answers = {}
    for row in unscramble(contents).split("\n"):
        x, y = row.split(":")
        answers[int(x)] = int(y)
    return answers


def save_answer_file(answers: Dict[int, int]) -> None:
    serialized = "\n".join(f"{n}:{answer}" for (n, answer) in sorted(answers.items()))
    contents = scramble(serialized)

    with open(ANSWER_FILE, "wb") as f:
        f.write(contents)


def run_problem(n: int) -> int:
    module = import_module(f"problems.{filename(n)}")
    return module.solve_problem()


@dataclasses.dataclass
class Formatter:
    """
    Formats HTML problem descriptions into plain text
    """

    indent: int = 0
    buffer: str = ""

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
        elif tag.name == "sup":
            # TODO fractions are sometimes written as ^a/_b
            self.buffer += "^"
        elif tag.name == "sub":
            self.buffer += "_"
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
        elif tag.name == "sup":
            pass
        elif tag.name == "sub":
            pass
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
            self.buffer += str(element)
        else:
            raise Exception(f"UNRECOGNIZED ELEMENT: {element}")

    def output(self) -> str:
        return self.buffer.strip()


def get_problem_description(n: int) -> str:
    # TODO error handling (just capture from outside this fn)
    resp = requests.get(f"https://projecteuler.net/minimal={n}")
    soup = BeautifulSoup(resp.text.strip(), "html.parser")

    fmt = Formatter()
    fmt.consume(soup)
    return fmt.output()


# ==== CLI Commands ====


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument(
    "number",
    type=int,
)
def create(number: int) -> None:
    """Copy the template file into the expected location, unless it already exists"""
    dst_path = f"problems/{filename(number)}.py"
    if os.path.exists(dst_path):
        raise Exception(f"Refusing to overwrite existing file {dst_path}")

    with open(TEMPLATE_FILE, "r") as f:
        template_contents = f.read()

    output = template_contents.format(description=get_problem_description(number))

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(output)


@cli.command()
@click.argument(
    "number",
    type=int,
)
def run(number: int) -> None:
    """
    Run the solver and print the answer
    """
    answer = run_problem(number)
    print(answer)


@cli.command()
@click.argument(
    "number",
    type=int,
)
@click.option(
    "-f", "--force", is_flag=True, default=False, help="Overwrite existing answer"
)
def save(number: int, force: bool) -> None:
    """
    Solve the problem and save the answer to the answers file
    """
    answers = parse_answer_file()
    if number in answers and not force:
        raise Exception(f"Answer is already in list")

    new_answer = run_problem(number)
    old_answer = answers.get(number)
    if old_answer is not None and old_answer != new_answer:
        assert force, "shouldn't have been able to get here w/o --force"
        print(
            f"WARNING: overwriting value for problem {number}: "
            f"{old_answer} -> {new_answer}"
        )

    # Actually write the answer and save it
    answers[number] = run_problem(number)
    save_answer_file(answers)


@cli.command()
def show() -> None:
    """
    Show the entire answer list.
    This is nice for checking that I wrote scramble and unscramble correctly.
    """
    answers = parse_answer_file()
    for (n, answer) in answers.items():
        print(f"Problem #{n:04}: {answer}")


@cli.command()
@click.argument(
    "number",
    type=int,
    default=0,  # TODO: gross :(
)
def check(number: int) -> None:
    """
    Solve all problems and check if the answers match those in the cache.
    This is nice for checking the validity of any refactoring I'm doing.
    """
    saved_answers: Dict[int, int] = parse_answer_file()

    def check_single(n: int) -> None:
        saved = saved_answers[n]
        current = run_problem(n)
        if current == saved:
            print(f"Problem {n:04} is good!")
        else:
            raise Exception(
                f"Problem {n:04} failed: solver has {current}, cache has {saved}"
            )

    if number == 0:
        for n in saved_answers.keys():
            check_single(n)
    else:
        check_single(number)

@cli.command()
@click.argument(
    "number",
    type=int,
)
def time(number: int) -> None:
    """
    Run the indicated problem several times and give some stats on the timing.
    """
    # TODO: how to clear cached data more generally?
    from lib.primes import _PRIME_STATE

    run_times = []
    for i in range(10):
        # Clear the cache
        _PRIME_STATE.clear()
        # Run the problem
        start = perf_counter()
        run_problem(number)
        elapsed = perf_counter() - start
        run_times.append(elapsed)
        # Print to reassure the user something's happening
        print(f"Trial #{i+1}: {elapsed:.3f}s")

    print("Test complete!")
    print(f"Mean: {sum(run_times)/len(run_times)}")


if __name__ == "__main__":
    cli()
