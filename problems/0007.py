"""
By listing the first six prime numbers: 2, 3, 5, 7, 11, and 13, we can see that the 6th prime is 13.

What is the 10 001st prime number?
"""

from lib.misc import nth
from lib.prime_state import PrimeCache

N = 10_001


def solve_problem() -> int:
    pc = PrimeCache()
    return nth(pc.iter_primes(), N - 1)
