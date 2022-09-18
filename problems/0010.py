"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below two million.
"""


from lib.prime_state import PrimeCache


N = 2_000_000


def solve_problem() -> int:
    pc = PrimeCache()
    return sum(pc.iter_primes(cutoff=N))
