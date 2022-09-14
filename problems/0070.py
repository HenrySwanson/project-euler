"""
Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine
the number of positive numbers less than or equal to n which are relatively prime to n.
For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to
nine, φ(9)=6.

The number 1 is considered to be relatively prime to every positive number, so φ(1)=1. 

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and
the ratio n/φ(n) produces a minimum.
"""

import math
from lib.misc import to_digits
from lib.primes import init_primes_up_to, iter_primes, iter_primes_rev, totient


N = 10_000_000


def solve_problem() -> int:
    # We know that phi(n) gets smaller the more primes we have, and the smaller
    # they are. So we want big primes, and few of them.

    # We know 1 prime won't work, because phi(p) = p - 1, and since that'll change
    # the last digit from 1, 3, 7, 9 to 0, 2, 6, 8, and nothing else, we'll never
    # get a permutation of the original digits.

    # So we'll start with 2 primes. Start at sqrt(N) * sqrt(N) and work our way
    # down to the smaller primes.

    best = None  # n, n / phi(n)
    for p in iter_primes_rev(int(math.sqrt(N))):

        # quick check: is it even possible to get a better ratio here?
        min_possible_ratio = p / (p - 1)
        if best is not None and min_possible_ratio > best[1]:
            break

        for q in iter_primes_rev(N // p):
            n = p * q
            phi_n = (p - 1) * (q - 1) if p != q else p * (p - 1)
            ratio = n / phi_n

            # the ratio can only increase from here, so check if we should bail out
            if best is not None and n / phi_n > best[1]:
                break

            if not same_digits(n, phi_n):
                continue

            if best is None or ratio < best[1]:
                best = (n, ratio)

    # Well what about 3 primes?
    # The best we can do is p ~ cbrt(N); just assert that this is too large
    # already.
    p_cbrt = int(N ** (1 / 3))
    min_possible_ratio = (p / (p_cbrt - 1)) ** 3
    assert best[1] < min_possible_ratio

    assert best is not None
    return best[0]


def same_digits(a: int, b: int) -> bool:
    return sorted(to_digits(a)) == sorted(to_digits(b))
