"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 600851475143 ?
"""

from lib.prime_state import PrimeCache

N = 600851475143


def solve_problem() -> int:
    pc = PrimeCache()
    factors = sorted(pc.factor(N))
    return factors[-1].prime
