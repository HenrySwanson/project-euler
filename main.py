#!/usr/bin/env python

import os
from importlib import import_module
from time import perf_counter
from typing import Dict, Iterable, Optional, List, Tuple

import click
import requests
from cli.answer import parse_answer_file, save_answer_file

from cli.format import htmlToDocstring
from cli.intervals import format_as_intervals

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


def list_problem_files() -> List[int]:
    problems = []
    for file in os.listdir("problems"):
        try:
            problems.append(int(file.removesuffix(".py")))
        except ValueError:
            pass

    return problems


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
    """Use the template file to create a starting point for the given problem."""
    dst_path = f"problems/{filename(number)}.py"

    if os.path.exists(dst_path):
        click.confirm(
            f"File {dst_path} already exists; do you want to overwrite?", abort=True
        )

    with open(TEMPLATE_FILE, "r") as f:
        template_contents = f.read()

    output = template_contents.format(description=get_problem_description(number))

    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(output)

    click.echo(f"Created file for problem {number} at {dst_path}")


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
    click.secho(f"Answer: {answer}", bold=True)

    answers = parse_answer_file(ANSWER_FILE)
    old_answer = answers.get(number)

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
        answers[number] = answer
        save_answer_file(ANSWER_FILE, answers)
        click.echo("Saved!")


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

    problems = (
        set(list_problem_files()) | saved_answers.keys() if number == 0 else {number}
    )

    succeeded = failed = weird = unsolved = 0
    for n in problems:
        # Get current and saved answers
        saved = saved_answers.get(n)
        try:
            current = run_problem(n)
        except ImportError:
            current = None

        # Big ol' match statement
        if saved is None:
            if current is None:
                click.echo(f"Problem {n:04} is unsolved")
                unsolved += 1
            else:
                click.secho(
                    f"Problem {n:04} produces answer {current}, but it is not saved",
                    fg="yellow",
                )
                weird += 1
        else:
            if current is None:
                click.secho(
                    f"Problem {n:04} has a saved answer {saved}, but no solver",
                    fg="yellow",
                )
                weird += 1
            elif current == saved:
                click.secho(f"Problem {n:04} is good!", fg="green")
                succeeded += 1
            else:
                click.secho(
                    f"Problem {n:04} failed: solver has {current}, save file has {saved}",
                    fg="red",
                    bold=True,
                )
                failed += 1

    click.secho(
        f"Ran {len(problems)} problems: {succeeded} succeeded, {failed} failed, {unsolved} unsolved, {weird} need attention",
        fg="red" if failed > 0 else "yellow" if weird > 0 else "green",
    )


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
    "number",
    type=int,
)
def time(number: int) -> None:
    """
    Run the indicated problem several times and give some stats on the timing.
    """

    run_times = []
    for i in range(10):
        # Run the problem
        start = perf_counter()
        run_problem(number)
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
def show() -> None:
    """
    Show the entire answer list.
    This is nice for checking that I wrote scramble and unscramble correctly.
    """
    answers = parse_answer_file(ANSWER_FILE)
    for (n, answer) in answers.items():
        click.echo(f"Problem #{n:04}: {answer}")


@answers.command()
@click.argument("number", type=int)
def delete(number: int) -> None:
    """Delete a specific answer from the save file."""
    answers = parse_answer_file(ANSWER_FILE)
    if number in answers:
        click.confirm(
            f"Are you sure you want to delete the saved answer for problem {number}?",
            abort=True,
        )
        del answers[number]
        save_answer_file(ANSWER_FILE, answers)
    else:
        click.secho(f"No saved answer for problem {number}", fg="yellow")


if __name__ == "__main__":
    cli()
