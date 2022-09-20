"""
It is well known that if the square root of a natural number is not an integer, then it is irrational.
The decimal expansion of such square roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital sum of the first one hundred
decimal digits is 475.

For the first one hundred natural numbers, find the total of the digital sums of the first one hundred
decimal digits for all the irrational square roots.
"""

from decimal import Context, Decimal, localcontext
from math import isqrt

from lib.misc import is_perfect_square, to_digits


N = 100
PREC = 100


def solve_problem() -> int:
    big_pow_10 = 10**PREC

    total = 0
    for n in range(1, N + 1):
        if is_perfect_square(n):
            continue

        sqrt = isqrt(n * big_pow_10 * big_pow_10)

        # Now get the digits
        digits = to_digits(sqrt)[:PREC]
        total += sum(digits)

    return total
