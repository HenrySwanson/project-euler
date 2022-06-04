"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""

from lib.primes import iter_primes

N = 2_000_000


def solve_problem() -> int:
    total = 0
    for p in iter_primes():
        if p >= N:
            break
        total += p
    return total
