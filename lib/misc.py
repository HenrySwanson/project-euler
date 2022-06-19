import collections
import itertools
from lib2to3.pgen2.token import OP
import math
from typing import (
    Callable,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
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


def triangle(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 3
    return n * (n + 1) // 2


def pentagonal(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 5
    return n * (3 * n - 1) // 2


def hexagonal(n: int) -> int:
    return n * (2 * n - 1)


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


def lcm(a: int, b: int) -> int:
    # pyre-fixme[16]: Why does pyre think this doesn't exist? Wrong stdlib version?
    return math.lcm(a, b)


def to_digits(n: int) -> Iterator[int]:
    return iter(int(x) for x in str(n))


def from_digits(it: Iterable[int]) -> int:
    # TODO: is this really faster than arithmetic?
    return int("".join(str(d) for d in it))


def is_palindrome(n: int) -> bool:
    digits = list(to_digits(n))
    return digits == list(reversed(digits))


# TODO: don't like name :(
def increasing_seq_cache(f: Callable[[int], int]) -> Callable[[int], bool]:
    max_k: int = 0
    max_fk: int = f(0)
    cache: Set[int] = {max_fk}

    def inner(n: int) -> bool:
        nonlocal max_k, max_fk, cache
        while n > max_fk:
            max_k += 1
            max_fk = f(max_k)
            cache.add(max_fk)
        return n in cache

    return inner


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
    input: str, start_line: Optional[int], end_line: Optional[int]
) -> Tuple[Tuple[int, ...], ...]:
    return tuple(
        tuple(int(x) for x in line.split(" "))
        for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


# Copied from itertools recipes
def powerset(iterable: Iterable[T]) -> Iterable[Tuple[T, ...]]:
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(
        itertools.combinations(s, r) for r in range(len(s) + 1)
    )
