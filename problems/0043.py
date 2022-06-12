"""
The number, 1406357289, is a 0 to 9 pandigital number because it is made up of each of the digits 0 to 9 in some order, but it also has a rather interesting sub-string divisibility property.
Let d_1 be the 1^st digit, d_2 be the 2^nd digit, and so on. In this way, we note the following:
- d_2d_3d_4=406 is divisible by 2
- d_3d_4d_5=063 is divisible by 3
- d_4d_5d_6=635 is divisible by 5
- d_5d_6d_7=357 is divisible by 7
- d_6d_7d_8=572 is divisible by 11
- d_7d_8d_9=728 is divisible by 13
- d_8d_9d_10=289 is divisible by 17
Find the sum of all 0 to 9 pandigital numbers with this property.
"""


from itertools import permutations
import itertools
from typing import Iterator, List, Set, Tuple

from lib.misc import from_digits, to_digits

FACTOR_ORDER = [17, 13, 11, 7, 5, 3, 2]


def solve_problem() -> int:
    # Let's do some quick narrowing of possibilities
    # d_4 must be even
    # d_6 is 0 or 5
    # d_8 d_9 d_10 is quite constrained

    total = 0

    all_digits = set(range(10))
    for last_three in gen_triplets(FACTOR_ORDER[0], all_digits):
        allowed_digits = all_digits - set(last_three)
        for d1_to_d7 in recurse(
            last_three[0], last_three[1], FACTOR_ORDER[1:], allowed_digits
        ):
            total += from_digits(list(d1_to_d7) + list(last_three))

    return total


def gen_triplets(base: int, allowed_digits: Set[int]) -> Iterator[Tuple[int, int, int]]:
    for k in itertools.count():
        n = k * base
        if n >= 1000:
            return

        # Unpack into digits and left-pad with zeros
        digits = tuple(to_digits(n))
        digits = (0,) * (3 - len(digits)) + digits
        assert len(digits) == 3

        if len(set(digits)) < 3:
            continue

        if set(digits) <= allowed_digits:
            yield digits


def recurse(
    b: int, c: int, factors: List[int], allowed_digits: Set[int]
) -> Iterator[Tuple[int, ...]]:
    if not factors:
        assert len(allowed_digits) == 1
        yield tuple(allowed_digits)
        return

    for a in allowed_digits:
        n = from_digits([a, b, c])
        if n % factors[0] == 0:
            # Then a is good! Let's recurse with it
            for header in recurse(a, b, factors[1:], allowed_digits - {a}):
                yield header + (a,)
