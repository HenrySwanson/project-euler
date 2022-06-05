#!/usr/bin/env python

import itertools
import os
import shutil
from importlib import import_module
from typing import Dict

import click

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


def filename(n: int) -> str:
    return f"{n:04}"


# I put in some very basic fuckery here so that I'm not just writing a list of
# plaintext answers directly to GitHub.
# Is it unbreakable encryption? No. But if someone wants the answers from my repo
# they could just run the problem solvers anyways, so whatever.


def scramble(input: str) -> bytes:
    nonsense = itertools.count()
    return bytes(x ^ y for (x, y) in zip(input.encode(), nonsense))


def unscramble(input: bytes) -> str:
    nonsense = itertools.count()
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

    with open(ANSWER_FILE, "wb") as f:
        f.write(scramble(serialized))


def run_problem(n: int) -> int:
    module = import_module(f"problems.{filename(n)}")
    return module.solve_problem()


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

    shutil.copy(TEMPLATE_FILE, dst_path)


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
    saved_answers = parse_answer_file()

    def check_single(n):
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


if __name__ == "__main__":
    cli()
