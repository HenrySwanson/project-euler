import collections
import itertools
from lib2to3.pgen2.token import OP
import math
from typing import Iterable, Iterator, List, Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


def general_fibonacci_iter(a: int, b: int) -> Iterator[int]:
    yield a
    yield b
    while True:
        c = a + b
        yield c
        (a, b) = (b, c)


def fibonacci_iter() -> Iterator[int]:
    return general_fibonacci_iter(0, 1)


def nth(iterable: Iterable[T], n: int) -> T:
    return next(itertools.islice(iterable, n, None))


def triangle(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 3
    return n * (n + 1) // 2


def lcm(a: int, b: int) -> int:
    # pyre-fixme[16]: Why does pyre think this doesn't exist? Wrong stdlib version?
    return math.lcm(a, b)


def digits(n: int) -> Iterator[int]:
    return iter(int(x) for x in str(n))


# TODO: there's gotta be something in python that does this
def _ext_slice(s: Sequence[T], start: Optional[int], end: Optional[int]) -> Sequence[T]:
    if start is not None:
        if end is not None:
            return s[start:end]
        else:
            return s[start:]
    else:
        if end is not None:
            return s[:end]
        else:
            return s


def parse_numeric_list(
    input: str, start_line: Optional[int], end_line: Optional[int]
) -> Tuple[int]:
    return tuple(
        int(line) for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


def parse_numeric_grid(
    input: str, start_line: Optional[int], end_line: Optional[int]
) -> Tuple[Tuple[int]]:
    return tuple(
        tuple(int(x) for x in line.split(" "))
        for line in _ext_slice(input.splitlines(), start_line, end_line)
    )
