import itertools
from typing import Dict

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


def parse_answer_file(path: str) -> Dict[int, int]:
    with open(path, "rb") as f:
        contents: bytes = f.read()

    if not contents:
        return {}

    answers = {}
    for row in unscramble(contents).split("\n"):
        x, y = row.split(":")
        answers[int(x)] = int(y)
    return answers


def save_answer_file(path: str, answers: Dict[int, int]) -> None:
    serialized = "\n".join(f"{n}:{answer}" for (n, answer) in sorted(answers.items()))
    contents = scramble(serialized)

    with open(path, "wb") as f:
        f.write(contents)
