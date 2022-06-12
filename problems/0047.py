"""
The first two consecutive numbers to have two distinct prime factors are:
14 = 2 × 7
15 = 3 × 5
The first three consecutive numbers to have three distinct prime factors are:
644 = 2² × 7 × 23
645 = 3 × 5 × 43
646 = 2 × 17 × 19.
Find the first four consecutive integers to have four distinct prime factors each. What is the first of these numbers?
"""


import itertools
from lib.primes import init_primes_up_to, num_distinct_prime_factors


def solve_problem() -> int:
    init_primes_up_to(10000)

    count = 0
    for n in itertools.count(2 * 3 * 5 * 7):
        if num_distinct_prime_factors(n) == 4:
            count += 1
        else:
            count = 0

        if count == 4:
            return n - 3

    raise AssertionError()
