"""
Take the number 192 and multiply it by each of 1, 2, and 3:
    192 × 1 = 192
    192 × 2 = 384
    192 × 3 = 576
By concatenating each product we get the 1 to 9 pandigital, 192384576. We will call 192384576 the concatenated product of 192 and (1,2,3)
The same can be achieved by starting with 9 and multiplying by 1, 2, 3, 4, and 5, giving the pandigital, 918273645, which is the concatenated product of 9 and (1,2,3,4,5).
What is the largest 1 to 9 pandigital 9-digit number that can be formed as the concatenated product of an integer with (1,2, ... , n) where n> 1?
"""

from typing import Iterator, List
from lib.misc import digits as to_digits, from_digits


def solve_problem() -> int:
    # I think the only feasible patterns are:
    # 1 2 2 2 2
    # 1 1 1 2 2 2
    # 1 1 1 1 1 2 2
    # 1 1 1 1 1 1 1 2
    # 1 1 1 1 1 1 1 1 1 1
    # 2 2 2 3
    # 3 3 3
    # 4 5
    # Because 9 18 27 36 45 exists, we can rule out the other ones starting with 1.
    # So...
    best = concat_product(9, 5)
    assert is_pandigital(best)

    def gen_possible_candidates() -> Iterator[List[int]]:
        for n in range(10, 100):
            yield concat_product(n, 4)
        for n in range(100, 1000):
            yield concat_product(n, 3)
        for n in range(1000, 10000):
            yield concat_product(n, 2)

    for candidate in gen_possible_candidates():
        if is_pandigital(candidate) and candidate > best:
            best = candidate

    return from_digits(best)


def concat_product(base: int, n: int) -> List[int]:
    return [d for k in range(1, n + 1) for d in to_digits(base * k)]


def is_pandigital(digits: List[int]) -> bool:
    return sorted(digits) == list(range(1, 10))
