import itertools
import math
from typing import (
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)


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


def sum_of_n_squares(n: int) -> int:
    return n * (n + 1) * (2 * n + 1) // 6


def binomial(n: int, k: int) -> int:
    if not 0 <= k <= n:
        return 0

    if 2 * k > n:
        k = n - k

    num = math.prod(n - i for i in range(k))
    den = math.prod(i + 1 for i in range(k))
    assert num % den == 0
    return num // den


def to_digits(n: int) -> List[int]:
    return [int(x) for x in str(n)]


def from_digits(it: Iterable[int]) -> int:
    # TODO: is this really faster than arithmetic?
    return int("".join(str(d) for d in it))


def num_digits(n: int) -> int:
    assert n > 0, "Input must be positive"
    return int(math.log10(n)) + 1


def is_palindrome(n: int) -> bool:
    digits = to_digits(n)
    return digits == list(reversed(digits))


def is_perfect_square(n: int) -> bool:
    x = int(math.sqrt(n))
    return x * x == n


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
) -> Tuple[int, ...]:
    return tuple(
        int(line) for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


def parse_numeric_grid(
    input: str, start_line: Optional[int], end_line: Optional[int], sep: str = " "
) -> Tuple[Tuple[int, ...], ...]:
    return tuple(
        tuple(int(x) for x in line.split(sep))
        for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


# Copied from itertools recipes
def powerset(iterable: Iterable[T]) -> Iterable[Tuple[T, ...]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )
