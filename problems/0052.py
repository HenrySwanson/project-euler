"""
It can be seen that the number, 125874, and its double, 251748, contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and 6x, contain the same digits.
"""


import itertools

from lib.misc import to_digits

N = 6


def solve_problem() -> int:
    # If x and 6x contain the same digits, then in particular they have the same
    # number of digits.
    # So 10^k <= x < 10^k * 10/6
    for k in itertools.count(1):
        lower = 10**k
        upper = int(lower * 10 / 6)
        for x in range(lower, upper + 1):
            digits = sorted(to_digits(x))
            if all(digits == sorted(to_digits(i * x)) for i in range(2, N + 1)):
                return x

    raise AssertionError()


# In hindsight, lol I actually knew this fact ahead of time. Oh well.
