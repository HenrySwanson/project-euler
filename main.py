#!/usr/bin/env python

from collections import defaultdict
import enum
import os
from importlib import import_module
from sre_constants import FAILURE, SUCCESS
from time import perf_counter
from typing import Dict, List, Optional, Set, Tuple

import click
import requests
from cli.answer import parse_answer_file, save_answer_file

from cli.format import htmlToDocstring
from cli.intervals import format_as_intervals, parse_interval_string

TEMPLATE_FILE = "problem.py.template"
ANSWER_FILE = "answers.bin"

# ==== TODO LIST ====
# - tests
# - can i do some python deepmagic to detect the '...' in the problem file?
#   might help with distinguishing "downloaded" from "started"


class CheckStatus(enum.Enum):
    SUCCESS = enum.auto()
    FAILURE = enum.auto()
    UNSOLVED = enum.auto()
    NEEDS_ATTENTION = enum.auto()


def filename(n: int) -> str:
    return f"{n:04}"


def run_problem(n: int) -> int:
    module = import_module(f"problems.{filename(n)}")
    return module.solve_problem()


def get_problem_description(n: int) -> str:
    """
    Fetch the project description from the Project Euler website, and apply some light formatting.
    """
    
    # TODO error handling (just capture from outside this fn)
    resp = requests.get(f"https://projecteuler.net/minimal={n}")
    return htmlToDocstring(resp.text)


def list_problem_files() -> List[int]:
    """
    Returns a list of integers for which a solver file exists.
    """

    problems = []
    for file in os.listdir("problems"):
        try:
            problems.append(int(file.removesuffix(".py")))
        except ValueError:
            pass

    return problems


def parse_interval_input(args: Tuple[str]) -> Tuple[Set[int], bool]:
    """
    Returns a set of integers that are explicitly specified by the user, and also
    a boolean indicating whether "all" was passed.
    (The caller likely wants to handle that themselves.)
    """

    problems = set()
    include_all = False

    for arg in args:
        if arg == "all":
            include_all = True
        else:
            (start, end) = parse_interval_string(arg)
            problems.update(range(start, end + 1))

    return problems, include_all


# ==== CLI Commands ====


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("problems", type=str, nargs=-1, required=True)
def create(problems: Tuple[str]) -> None:
    """Use the template file to create a starting point for the given problems."""

    numbers, include_all = parse_interval_input(problems)
    if include_all:
        raise click.Abort('"all" not valid argument for `create` command')

    for n in numbers:
        try:
            create_single_file(n)
        except Exception as e:
            click.secho(f"Unable to create file for problem {n}: {e}", fg="red")
            pass


def create_single_file(n: int) -> None:
    """Creates a solver file for the given problem."""

    dst_path = f"problems/{filename(n)}.py"

    if os.path.exists(dst_path):
        if not click.confirm(
            f"File {dst_path} already exists; do you want to overwrite?"
        ):
            return

    with open(TEMPLATE_FILE, "r") as f:
        template_contents = f.read()

    output = template_contents.format(description=get_problem_description(n))

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(output)

    click.echo(f"Created file for problem {n} at {dst_path}")


@cli.command()
@click.argument("problems", type=str, nargs=-1, required=True)
def run(problems: Tuple[str]) -> None:
    """Run the solver for the given problems and print the answer."""

    numbers, include_all = parse_interval_input(problems)
    if include_all:
        numbers.update(list_problem_files())

    for n in numbers:
        run_single_problem(n)
        click.echo()


def run_single_problem(n: int) -> None:
    """
    Runs a single problem, showing its output to the user, and prompting the
    user to save if the answer is not already saved.
    """

    click.echo(f"Running problem {n:04}...")
    answer = run_problem(n)
    click.secho(f"Answer: {answer}", bold=True)

    answers = parse_answer_file(ANSWER_FILE)
    old_answer = answers.get(n)

    if old_answer is None:
        click.echo("No previously saved answer")
    elif old_answer == answer:
        click.secho("Answer matches previously saved answer", fg="green")
    else:
        click.secho(
            f"WARNING: answer does not match previously saved answer {old_answer}!",
            fg="red",
        )

    if old_answer != answer and click.confirm("Would you like to save this answer?"):
        # Actually write the answer and save it
        answers[n] = answer
        save_answer_file(ANSWER_FILE, answers)
        click.echo("Saved!")


@cli.command()
@click.argument("problems", type=str, nargs=-1, required=True)
def check(problems: Tuple[str]) -> None:
    """
    Solve all problems and check if the answers match those in the cache.
    This is nice for checking the validity of any refactoring I'm doing.
    """

    # Figure out which problems the user specified
    numbers, include_all = parse_interval_input(problems)

    saved_answers: Dict[int, int] = parse_answer_file(ANSWER_FILE)

    if include_all:
        numbers.update(list_problem_files(), saved_answers.keys())

    statuses = defaultdict(int)
    for n in numbers:
        status = check_single_problem(n, saved_answers.get(n))
        statuses[status] += 1

    # Decide what color the summary message should show up as
    if statuses[CheckStatus.FAILURE] > 0:
        color = "red"
    elif statuses[CheckStatus.NEEDS_ATTENTION] > 0:
        color = "yellow"
    else:
        color = "green"

    click.secho(
        "Ran {num_problems} problems: {succeeded} succeeded, {failed} failed, {unsolved} unsolved, {attention} need attention".format(
            num_problems=len(numbers),
            succeeded=statuses[CheckStatus.SUCCESS],
            failed=statuses[CheckStatus.FAILURE],
            unsolved=statuses[CheckStatus.UNSOLVED],
            attention=statuses[CheckStatus.NEEDS_ATTENTION],
        ),
        fg=color,
    )


def check_single_problem(n: int, saved_answer: Optional[int]) -> CheckStatus:
    """
    Checks the status of a single problem against the saved answer, and returns
    a `CheckStatus` enum.
    """

    try:
        current_answer = run_problem(n)
    except ImportError:
        current_answer = None

    # Big ol' match statement
    if saved_answer is None:
        if current_answer is None:
            click.echo(f"Problem {n:04} is unsolved")
            return CheckStatus.UNSOLVED
        else:
            click.secho(
                f"Problem {n:04} produces answer {current_answer}, but it is not saved",
                fg="yellow",
            )
            return CheckStatus.NEEDS_ATTENTION
    else:
        if current_answer is None:
            click.secho(
                f"Problem {n:04} has a saved answer {saved_answer}, but no solver",
                fg="yellow",
            )
            return CheckStatus.NEEDS_ATTENTION
        elif current_answer == saved_answer:
            click.secho(f"Problem {n:04} is good!", fg="green")
            return CheckStatus.SUCCESS
        else:
            click.secho(
                f"Problem {n:04} failed: solver has {current_answer}, save file has {saved_answer}",
                fg="red",
                bold=True,
            )
            return CheckStatus.FAILURE


@cli.command()
def overview() -> None:
    """
    Check which problems have been done and which are not.

    Helpful for checking if I forgot to save an answer.
    """

    problems_saved = parse_answer_file(ANSWER_FILE).keys()
    problems_with_files = set(list_problem_files())

    click.echo("Problems solved:")
    click.echo(format_as_intervals(problems_with_files & problems_saved))

    click.echo("Problems downloaded and unsolved:")
    click.echo(format_as_intervals(problems_with_files - problems_saved))

    if not problems_saved <= problems_with_files:
        click.echo("Problems solved but not downloaded (???):")
        click.echo(format_as_intervals(problems_saved - problems_with_files))

    problems_known = problems_with_files | problems_saved
    first_unknown = max(problems_known) + 1 if problems_known else 1
    click.echo("Problems remaining:")
    click.echo(
        format_as_intervals(
            set(range(1, first_unknown)) - problems_known, infinite_tail=first_unknown
        )
    )


@cli.command()
@click.argument(
    "problem",
    type=int,
)
def time(problem: int) -> None:
    """
    Run the indicated problem several times and give some stats on the timing.
    """

    run_times = []
    for i in range(10):
        # Run the problem
        start = perf_counter()
        run_problem(problem)
        elapsed = perf_counter() - start
        run_times.append(elapsed)
        # Print to reassure the user something's happening
        click.echo(f"Trial #{i+1}: {elapsed:.3f}s")

    click.echo("Test complete!")
    click.echo(f"Mean: {sum(run_times)/len(run_times):.3f}")


@cli.group()
def answers() -> None:
    """
    Commands for manipulating the answer save file.
    """
    pass


@answers.command()
@click.argument("problems", type=str, nargs=-1, required=True)
def show(problems: Tuple[str]) -> None:
    """
    Show specific answers from the answer list.
    This is nice for checking that I wrote scramble and unscramble correctly.
    """

    numbers, include_all = parse_interval_input(problems)
    answers = parse_answer_file(ANSWER_FILE)

    if include_all:
        numbers.update(answers.keys())

    for n in numbers:
        answer = answers[n]
        click.echo(f"Problem #{n:04}: {answer}")


@answers.command()
@click.argument("problem", type=int)
def delete(problem: int) -> None:
    """Delete a specific answer from the save file."""

    answers = parse_answer_file(ANSWER_FILE)
    if problem in answers:
        click.confirm(
            f"Are you sure you want to delete the saved answer for problem {problem}?",
            abort=True,
        )
        del answers[problem]
        save_answer_file(ANSWER_FILE, answers)
    else:
        click.secho(f"No saved answer for problem {problem}", fg="yellow")


if __name__ == "__main__":
    cli()
