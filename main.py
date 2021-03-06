#!/usr/bin/env python

import os
from importlib import import_module
from time import perf_counter
from typing import Dict

import click
import requests
from cli.answer import parse_answer_file, save_answer_file

from cli.format import htmlToDocstring

TEMPLATE_FILE = "problem.py.template"
ANSWER_FILE = "answers.bin"

# ==== TODO LIST ====
# - maybe make scramble and unscramble depend on an un-checked-in file
#   that i can conjure from memory?
#   - nah, too much effort
# - tests
# - if i forget to save, how can i run a command to check that?
# - `next` command?
# - an interactive mode would be cool!
#  - open 25, create, run, run, ..., run, save
#  - would have to force a reload of all py files though...
# - run and check are pretty similar, it'd be nice to have them unified
#   - both run the solver, and the only difference is whether there's an answer already saved


def filename(n: int) -> str:
    return f"{n:04}"


def run_problem(n: int) -> int:
    module = import_module(f"problems.{filename(n)}")
    return module.solve_problem()


def get_problem_description(n: int) -> str:
    # TODO error handling (just capture from outside this fn)
    resp = requests.get(f"https://projecteuler.net/minimal={n}")
    return htmlToDocstring(resp.text)


# ==== CLI Commands ====


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument(
    "number",
    type=int,
)
@click.option(
    "-f", "--force", is_flag=True, default=False, help="Overwrite existing answer"
)
def create(number: int, force: bool) -> None:
    """Copy the template file into the expected location, unless it already exists"""
    dst_path = f"problems/{filename(number)}.py"
    if os.path.exists(dst_path) and not force:
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
@click.option("-s", "--save", is_flag=True, default=False, help="Save answer to file")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    default=False,
    help="If saving, save even if there's already an answer in the file",
)
def run(number: int, save: bool, force: bool) -> None:
    """
    Run the solver and print the answer
    """
    answer = run_problem(number)
    print(answer)

    if not save:
        return

    answers = parse_answer_file(ANSWER_FILE)
    if number in answers and not force:
        raise Exception(f"Answer is already in list")

    old_answer = answers.get(number)
    if old_answer is not None and old_answer != answer:
        assert force, "shouldn't have been able to get here w/o --force"
        print(
            f"WARNING: overwriting value for problem {number}: "
            f"{old_answer} -> {answer}"
        )

    # Actually write the answer and save it
    answers[number] = answer
    save_answer_file(ANSWER_FILE, answers)


@cli.command()
def show() -> None:
    """
    Show the entire answer list.
    This is nice for checking that I wrote scramble and unscramble correctly.
    """
    answers = parse_answer_file(ANSWER_FILE)
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
    saved_answers: Dict[int, int] = parse_answer_file(ANSWER_FILE)

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
    print(f"Mean: {sum(run_times)/len(run_times):.3f}")


if __name__ == "__main__":
    cli()
