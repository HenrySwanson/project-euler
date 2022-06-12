"""
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.
9 = 7 + 2×1^2
15 = 7 + 2×2^2
21 = 3 + 2×3^2
25 = 7 + 2×3^2
27 = 19 + 2×2^2
33 = 31 + 2×1^2
It turns out that the conjecture was false.
What is the smallest odd composite that cannot be written as the sum of a prime and twice a square?
"""


import itertools

from lib.primes import is_prime, iter_primes


def solve_problem() -> int:
    # Let's do this in a zig-zaggy way. Generate all combinations of the first
    # k primes and the first k squares.
    frontier = 0  # The minimum possible number we can now generate
    k = 0

    # Composites we've seen so far
    composites = set()

    for n in itertools.count(3, step=2):
        if is_prime(n):
            continue

        while frontier < n:
            # Expand our horizons:
            k += 1
            primes = list(itertools.islice(iter_primes(), 0, k))
            p_max = primes[-1]
            sq_max = k * k  # 1-indexed
            for p in primes:
                composites.add(p + 2 * sq_max)
            for i in range(1, k + 1):
                composites.add(p_max + 2 * i * i)

            # We can no longer generate numbers smaller than p_max and 2 * sq_max
            frontier = min(p_max, 2 * sq_max)

        if n not in composites:
            return n

    raise AssertionError()
