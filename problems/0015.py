"""
Starting in the top left corner of a 2×2 grid, and only being able to move to the right and down, there are exactly 6 routes to the bottom right corner.

How many such routes are there through a 20×20 grid?
"""

from math import comb


N = 20


def solve_problem() -> int:
    # No brute force, only math here. This is a combinatorics problem. We'll always make N steps
    # right and N steps down. The only question is one of ordering. It's 2N choose N.
    return comb(2 * N, N)
    ...
