"""
A unit fraction contains 1 in the numerator. The decimal representation of the unit fractions with denominators 2 to 10 are given:

    1/2	= 	0.5
    1/3	= 	0.(3)
    1/4	= 	0.25
    1/5	= 	0.2
    1/6	= 	0.1(6)
    1/7	= 	0.(142857)
    1/8	= 	0.125
    1/9	= 	0.(1)
    1/10	= 	0.1 

Where 0.1(6) means 0.166666..., and has a 1-digit recurring cycle. It can be seen that 1/7 has a 6-digit recurring cycle.

Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
"""

import itertools


def solve_problem() -> int:
    return max(range(1, 1000), key=get_cycle_length)


def get_cycle_length(n: int) -> int:
    # Number theory time

    # The repeated section of the decimal comes from 1/n = x/999...999. So we want to multiply
    # n by something until we get 10^k - 1.
    # But, more cleanly, what we can do is check whether 10^k-1 is a multiple of n for each k.

    # Also, watch out for n not coprime to 10. Strip out the 2s and 5s first.
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5

    # Now search for k
    for k in itertools.count(1):
        if (10**k - 1) % n == 0:
            return k

    raise AssertionError()
