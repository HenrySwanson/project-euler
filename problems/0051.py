"""
By replacing the 1^st digit of the 2-digit number *3, it turns out that six of the nine possible values: 13, 23, 43,
53, 73, and 83, are all prime.

By replacing the 3^rd and 4^th digits of 56**3 with the same digit, this 5-digit number is the first example having
seven primes among the ten generated numbers, yielding the family: 56003, 56113, 56333, 56443, 56663, 56773, and 56993.
Consequently 56003, being the first member of this family, is the smallest prime with this property.

Find the smallest prime which, by replacing part of the number (not necessarily adjacent digits) with the same digit,
is part of an eight prime value family.
"""


import itertools
from collections import defaultdict
from typing import Iterator, Optional

from lib.misc import powerset, to_digits
from lib.primes import iter_primes

N = 8


def solve_problem() -> int:
    for n in itertools.count(1):
        p = solve_problem_n(n)
        if p is not None:
            return p

    raise AssertionError()


def solve_problem_n(n: int) -> Optional[int]:
    # Group all the primes by their digit patterns
    # For example, 14411 would fall under X44XX and 1XX11
    # But also! 1X411, 14X11, X4411, X44X1, X441X, etc
    buckets = defaultdict(list)

    lower = 10**n
    upper = lower * 10
    for p in iter_primes(upper):
        if p < lower:
            continue

        for pattern in patterns(p):
            bucket = buckets[pattern]
            bucket.append(p)

            if len(bucket) >= N:
                return min(bucket)

    return None


def patterns(p: int) -> Iterator[str]:
    digits = list(to_digits(p))

    # Split up digits
    counts = [[] for _ in range(10)]
    for (i, d) in enumerate(digits):
        counts[d].append(i)

    for idxs in counts:
        if not idxs:
            continue

        for subset in powerset(idxs):
            yield "".join(
                "X" if i in subset else str(d) for (i, d) in enumerate(digits)
            )
