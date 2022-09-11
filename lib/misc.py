from fractions import Fraction
import itertools
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


def square(n: int) -> int:
    return n * n


def pentagonal(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 5
    return n * (3 * n - 1) // 2


def hexagonal(n: int) -> int:
    return n * (2 * n - 1)


def heptagonal(n: int) -> int:
    return n * (5 * n - 3) // 2


def octagonal(n: int) -> int:
    return n * (3 * n - 2)


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


def increasing_seq_cutoff(f: Callable[[int], int], start: int, end: int) -> List[int]:
    assert start <= end
    values = []
    for n in itertools.count(0):
        value = f(n)
        if value < start:
            continue
        if value >= end:
            break
        values.append(value)

    return values


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


def is_perfect_square(n: int) -> bool:
    x = int(math.sqrt(n))
    return x * x == n


# TODO: class for quadratic cfrac?
def cfrac_of_sqrt(n: int) -> Tuple[List[int], List[int]]:
    # First, check that d is not a perfect square.
    if is_perfect_square(n):
        # TODO maybe allow terminating cfracs?
        raise ValueError("perfect square!")

    # We want to track a number of the form (a + b * sqrt(n) / d)
    # and repeatedly find its continued fraction.
    sqrt_n = math.sqrt(n)

    a = 0
    b = 1
    d = 1
    history = []

    coeffs = []

    # Quadratics should repeat eventually, so this terminates
    while (a, b, d) not in history:
        history.append((a, b, d))

        # Get the integer part
        # (a+bX)/d = _ + (a'+bX)/d
        int_part = int((a + b * sqrt_n) / d)
        a -= int_part * d
        coeffs.append(int_part)

        # Now flip that fraction over, and rationalize the denominator
        # d/(a+bX) = d(-a+bX)/(b^2 n - a^2)
        # This will never be zero in the denominator, because that would
        # mean -a+bX is zero, i.e., X = a/b, and we know X is not a square.
        (a, b, d) = (-d * a, d * b, b * b * n - a * a)

        # Check for common denominators
        g = math.gcd(a, b, d)
        (a, b, d) = (a // g, b // g, d // g)

    # Where did we see this number before? That's the first coefficent that
    # we repeat
    idx = history.index((a, b, d))
    return (coeffs[:idx], coeffs[idx:])


def cfrac_tup_to_iter(cfrac: Tuple[List[int], List[int]]) -> Iterable[int]:
    head, tail = cfrac
    return itertools.chain(head, itertools.cycle(tail))


def nth_convergent(coeffs: Iterable[int], depth: int) -> Fraction:
    # Get the right number of coefficients
    coeffs = list(itertools.islice(coeffs, 0, depth))

    value = Fraction(coeffs[-1])
    for c in reversed(coeffs[:-1]):
        value = c + 1 / value

    return value


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
