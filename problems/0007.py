"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?
"""

from lib.misc import nth
from lib.primes import iter_primes

N = 10_001


def solve_problem() -> int:
    return nth(iter_primes(), N - 1)
