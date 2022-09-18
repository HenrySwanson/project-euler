"""
Euler discovered the remarkable quadratic formula:
    n^2 + n + 41

It turns out that the formula will produce 40 primes for the consecutive integer values 0 <= n <= 39. However, when n = 40, 40^2 + 40 + 41 = 40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41^2 + 41 + 41 is clearly divisible by 41.

The incredible formula n^2 - 79n + 1601 was discovered, which produces 80 primes for the consecutive values 0 <= n <= 79. The product of the coefficients, −79 and 1601, is −126479.

Considering quadratics of the form:
    n^2 + an + b, where |a| < 1000 and |b| <= 1000
    where |n| is the modulus/absolute value of n
    e.g. |11| = 11 and |-4| = 4

Find the product of the coefficients, a and b, for the quadratic expression that produces the maximum number of primes for consecutive values of n, starting with n = 0.
"""

import itertools
from lib.prime_state import PrimeCache


N = 1000


def solve_problem() -> int:
    pc = PrimeCache()

    best = (0, 0)
    best_score = 0

    # For p(0) to be prime, b must be prime. Also, since we're considering only positive primes,
    # b must be positive.
    for b in range(N + 1):
        if not pc.is_prime(b):
            continue

        # Also, because p(1) needs to be a positive prime, 1 + a + b needs to be a positive prime
        # too.
        for p in pc.iter_primes():
            a = p - b - 1
            # a will increase from 1-b to infinity, so cut it off to the right range
            if a <= -N:
                continue
            if a >= N:
                break

            score = test_quadratic(pc, a, b)
            if score > best_score:
                best = (a, b)
                best_score = score

    return best[0] * best[1]


def test_quadratic(pc: PrimeCache, a: int, b: int) -> int:
    for n in itertools.count():
        if not pc.is_prime(n * n + a * n + b):
            return n

    raise AssertionError()
