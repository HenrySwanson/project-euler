"""
It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?
"""


import itertools
from lib.prime_state import PrimeCache

N = 5000


def solve_problem() -> int:
    # Well this seems hard...

    # As a generating function, the normal partition function is:
    #   f(x) = (1 + x + x^2 + ...)(1 + x^2 + x^4 + ...)(1 + x^3 + x^6 + ...)
    # because each partition selects some number of 1s, some number of 2s, etc.
    # This condenses to:
    #   f(x) = prod_(k in N) 1 / (1 - x^k)

    # So I guess what we want is:
    #   f(x) = prod_(p prime) 1 / (1 - x^p)
    # Seems unfruitful.

    # Dynamic programming?
    #
    # Let f(S, p) be the number of ways to make a prime partition of S with parts <= p
    # Then, there are two ways to make a partition with parts <= p:
    # - only use primes < p
    # - use one p, and partitions of S - p with parts <= p
    # So f(S, p) = f(S, p - 1) + f(S - p, p)

    pc = PrimeCache()

    cache = {}  # f(S, p)
    cache_max = {0: 1, 1: 0}  # f(S)

    for n in itertools.count(2):
        # Find the number of prime partitions of n, by successively computing
        # f(S, p), and building up the cache.
        prev_p = None
        for p in pc.iter_primes(cutoff=n + 1):
            if prev_p is None:
                assert p == 2
                cache[(n, p)] = 1 if n % 2 == 0 else 0
            else:
                # We'd like to just say that second term is cache[(n - p, p)],
                # but what if p is much larger than n - p?
                # Then we'd never have that entry in cache.
                #
                # So we'll pick up the max value of cache[(n - p, _)]
                second_term = cache[(n - p, p)] if p <= n - p else cache_max[n - p]
                cache[(n, p)] = cache[(n, prev_p)] + second_term

            if cache[(n, p)] >= N:
                return n

            prev_p = p
            cache_max[n] = cache[(n, p)]

    raise AssertionError()
