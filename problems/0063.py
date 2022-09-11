"""
The 5-digit number, 16807=7^5, is also a fifth power. Similarly, the 9-digit number,
134217728=8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?
"""


import itertools

from lib.misc import num_digits


def solve_problem() -> int:
    # Well this is one of those "find the bound yourself" problems.
    #
    # If A is a k-digit number, then A^n has between n(k-1)+1 and nk digits.
    # So for A^n to be a n-digit number, then n must lie between those bounds.
    #
    # The first bound gives n(k-2) <= -1, i.e., k = 1.
    # Oh. Of course. 10^k has k+1 digits...
    #
    # Okay, when does the nth-power stop becoming n digits long? That can
    # be answered experimentally.

    total = 0
    for d in range(1, 10):
        for n in itertools.count(1):
            val = d**n
            if num_digits(val) == n:
                total += 1
            if num_digits(val) < n:
                break

    return total
