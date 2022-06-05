"""
The following iterative sequence is defined for the set of positive integers:

n → n/2 (n is even)
n → 3n + 1 (n is odd)

Using the rule above and starting with 13, we generate the following sequence:
13 → 40 → 20 → 10 → 5 → 16 → 8 → 4 → 2 → 1

It can be seen that this sequence (starting at 13 and finishing at 1) contains 10 terms. Although it has not been proved yet (Collatz Problem), it is thought that all starting numbers finish at 1.

Which starting number, under one million, produces the longest chain?

NOTE: Once the chain starts the terms are allowed to go above one million.
"""

from typing import Dict


def solve_problem() -> int:
    # EZ caching problem
    cache = {}
    for n in range(1, 1_000_001):
        collatz_length(n, cache)

    return max(cache.items(), key=lambda tup: tup[1])[0]


def collatz_length(n: int, cache: Dict[int, int]) -> int:
    if n in cache:
        return cache[n]

    if n == 1:
        result = 1
    else:
        k = n // 2 if n % 2 == 0 else 3 * n + 1
        result = collatz_length(k, cache) + 1

    cache[n] = result
    return result
