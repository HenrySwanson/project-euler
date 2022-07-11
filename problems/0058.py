"""
Starting with 1 and spiralling anticlockwise in the following way, a square spiral with side length 7 is formed.

37 36 35 34 33 32 31
38 17 16 15 14 13 30
39 18  5  4  3 12 29
40 19  6  1  2 11 28
41 20  7  8  9 10 27
42 21 22 23 24 25 26
43 44 45 46 47 48 49

It is interesting to note that the odd squares lie along the bottom right diagonal, but what is more interesting
is that 8 out of the 13 numbers lying along both diagonals are prime; that is, a ratio of 8/13 ≈ 62%.

If one complete new layer is wrapped around the spiral above, a square spiral with side length 9 will be formed.
If this process is continued, what is the side length of the square spiral for which the ratio of primes along
both diagonals first falls below 10%?
"""


import itertools

from lib.primes import is_prime


def solve_problem() -> int:
    # The same square is described in #28, and the numbers on the diagonals are
    #   X, (X - 2k), (X - 4k), (X - 6k)    where X = (2k+1)^2

    count = 1
    primes = 0
    for k in itertools.count(1):
        X = (2 * k + 1) * (2 * k + 1)
        count += 4
        primes += sum(1 for n in [X, X - 2 * k, X - 4 * k, X - 6 * k] if is_prime(n))

        if primes * 10 < count:
            return 2 * k + 1

    raise AssertionError()
