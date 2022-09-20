"""
Let p(n) represent the number of different ways in which n coins can be separated into piles. For example, five coins can be separated into piles in exactly seven different ways, so p(5)=7.

OOOOO
OOOO O
OOO OO
OOO O O
OO OO O
OO O O O
O O O O O

Find the least value of n for which p(n) is divisible by one million.
"""


import itertools
from typing import Dict, List, Optional

from lib.sequence import partition, pentagonal


def solve_problem() -> int:
    cache = {}
    for i in itertools.count(1):
        p_n = partition_mod(i, 1_000_000, cache)
        if p_n == 0:
            return i

    raise AssertionError()


def partition_mod(n: int, mod: int, cache: Dict[int, int]) -> int:
    # We use the recurrence relation to compute this
    if n < 0:
        return 0
    if n == 0:
        return 1

    if n in cache:
        return cache[n]

    total = 0
    for i in itertools.count(1):
        sign = 1 if i % 2 == 1 else -1

        p_k = pentagonal(i)
        total += sign * partition_mod(n - p_k, mod, cache)

        p_k = pentagonal(-i)
        total += sign * partition_mod(n - p_k, mod, cache)

        total %= mod

        if p_k >= n:
            break

    cache[n] = total
    return total
