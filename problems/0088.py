"""
A natural number, N, that can be written as the sum and product of a given set of at least two natural numbers, {a_1, a_2, ... , a_k} is called a product-sum number: N = a_1 + a_2 + ... + a_k = a_1 × a_2 × ... × a_k.

For example, 6 = 1 + 2 + 3 = 1 × 2 × 3.

For a given set of size, k, we shall call the smallest N with this property a minimal product-sum number. The minimal product-sum numbers for sets of size, k = 2, 3, 4, 5, and 6 are as follows.

k=2: 4 = 2 × 2 = 2 + 2
k=3: 6 = 1 × 2 × 3 = 1 + 2 + 3
k=4: 8 = 1 × 1 × 2 × 4 = 1 + 1 + 2 + 4
k=5: 8 = 1 × 1 × 2 × 2 × 2 = 1 + 1 + 2 + 2 + 2
k=6: 12 = 1 × 1 × 1 × 1 × 2 × 6 = 1 + 1 + 1 + 1 + 2 + 6

Hence for 2≤k≤6, the sum of all the minimal product-sum numbers is 4+6+8+12 = 30; note that 8 is only counted once in the sum.

In fact, as the complete set of minimal product-sum numbers for 2≤k≤12 is {4, 6, 8, 12, 15, 16}, the sum is 61.

What is the sum of all the minimal product-sum numbers for 2≤k≤12000?
"""

import itertools
from math import isqrt, prod, sqrt
from typing import Iterator, List, Tuple

from lib.prime_state import PrimeCache

MAX_K = 12_000

# How far do we have to search? Equivalently, for any k, what N do we need to search to
# to guarantee we've found *some* k product-sum number?
#
# If N = ab, then you can write N as a product-sum number like so:
#     a * b * (r copies of 1) = a + b + (r copies of 1), r = (ab - a - b) = (a - 1)*(b - 1)-1
#
# So ab needs to be a non-trivial factorization of N, and we get a decomposition with r+2 numbers.
# If we have N = 2k, then r = N-2, and the factorization is 1+1+...+1+2+N/2.
#
# So we only need to check up to N = 2 * MAX_K
MAX_N = MAX_K * 2


def solve_problem() -> int:
    minimals = [None] * (MAX_K + 1)
    misses = 0
    total = 0

    # We iterate through tuples (a_1, a_2, ...) where the product is <= MAX_N
    # and each a_i > 1.
    for tup in iter_tuples():
        # These tuples probably aren't product-sum decompositions; since each
        # a_i > 1, the sum is less than the product.
        # So we tack on a whole bunch of 1s to inflate the sum without affecting
        # the product (which btw is n).
        n = prod(tup)
        sum_tup = sum(tup)
        num_of_ones = n - sum_tup
        k = len(tup) + num_of_ones

        # Now put that into our map
        total += 1
        if k >= len(minimals):
            misses += 1
            continue

        current = minimals[k]
        if current is None or n < current:
            minimals[k] = n

    # It's about half of them right now, but we're down to 0.5s, so don't
    # sweat it.
    print(f"{total} total tuples, {misses} had k too large")

    return sum(set(minimals[2:]))


def iter_tuples() -> Iterator[Tuple[int, ...]]:
    return iter_tuples_helper(1, 2)


def iter_tuples_helper(
    product_so_far: int, min_factor: int
) -> Iterator[Tuple[int, ...]]:
    # Empty tuple is always allowed (i.e., yield what the parent
    # has so far).
    yield tuple()

    # Produce tuples in ascending order
    for n in itertools.count(min_factor):
        # Bail early if the product is too large
        new_product = n * product_so_far
        if new_product > MAX_N:
            return

        for tail in iter_tuples_helper(new_product, n):
            yield (n,) + tail
