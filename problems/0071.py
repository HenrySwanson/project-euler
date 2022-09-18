"""
Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d ≤ 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d ≤ 1,000,000 in ascending order of size, find the numerator of the fraction immediately to the left of 3/7.
"""

from math import gcd


N = 1_000_000


def solve_problem() -> int:
    # I recognize this as the Farey sequence.
    # Each term is the mediant of its neighbors, so just keep taking mediants until we see a denominator more than N
    a, b, c, d = 2, 5, 3, 7
    prev_a = None

    while b <= N:
        prev_a = a  # save for later

        a, b = (a + c, b + d)
        g = gcd(a, b)
        a, b = (a // g, b // g)

    assert prev_a is not None
    return prev_a
