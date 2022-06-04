#!/usr/bin/env python

import argparse
import os
import shutil
import itertools
from importlib import import_module
from typing import Dict, Iterator

TEMPLATE_FILE = "problem.py.template"
ANSWER_FILE = "answers.bin"

# ==== TODO LIST ====
# - check and show ignore the number argument. make that less bad
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


def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solve a Project Euler problem")
    parser.add_argument("number", type=int, help="which problem to solve")
    parser.add_argument(
        "action",
        type=str,
        choices=["run", "create", "save", "check", "show"],
        nargs="?",
        default="run",
    )
    return parser


def main() -> None:
    args = get_argparser().parse_args()

    n = args.number
    action = args.action

    if action == "run":
        # Solve the problem and print the answer
        answer = run_problem(n)
        print(answer)
    elif action == "create":
        # Copy the template file into the expected location, unless it already
        # exists.
        dst_path = f"problems/{filename(n)}.py"
        if os.path.exists(dst_path):
            raise Exception(f"Refusing to overwrite existing file {dst_path}")

        shutil.copy(TEMPLATE_FILE, dst_path)
    elif action == "save":
        # Solve the problem and save the answer to the answers file, unless it's
        # already there.
        answers = parse_answer_file()
        if n in answers:
            raise Exception(f"Answer is already in list")

        answers[n] = run_problem(n)
        save_answer_file(answers)
    elif action == "check":
        # Solve all problems and check if the answers match those in the cache.
        # This is nice for checking the validity of any refactoring I'm doing.
        saved_answers = parse_answer_file()
        for (n, saved) in saved_answers.items():
            current = run_problem(n)
            if current == saved:
                print(f"Problem {n:04} is good!")
            else:
                raise Exception(
                    f"Problem {n:04} failed: solver has {current}, cache has {saved}"
                )
    elif action == "show":
        # Show the entire answer list. This is nice for checking that I wrote
        # scramble and unscramble correctly.
        answers = parse_answer_file()
        for (n, answer) in answers.items():
            print(f"Problem #{n:04}: {answer}")
    else:
        raise Exception(f"Unexpected action '{action}'")


if __name__ == "__main__":
    main()
