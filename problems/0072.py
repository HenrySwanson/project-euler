"""
Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper fractions for d ≤ 1,000,000?
"""


from lib.prime_state import PrimeCache
from lib.primes import totient

N = 1_000_000


def solve_problem() -> int:
    # There is one fraction when n = 2, and beyond that, we add phi(n) fractions for each
    # increment of n.
    # Since phi(2) = 1, this can just be written as a sum of phi(n).
    pc = PrimeCache()
    pc.init_sieve_of_eratosthenes(N)

    # TODO: this is quite slow...
    return sum(totient(n, pc.factor(n)) for n in range(2, N + 1))
