"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.
{20,48,52}, {24,45,51}, {30,40,50}
For which value of p ≤ 1000, is the number of solutions maximised?
"""

from cmath import sqrt
from math import ceil

from lib.pythagorean import iter_primitive_pythagorean_by_perimeter


N = 1000


def solve_problem() -> int:
    solns = [0 for _ in range(N + 1)]

    for (a, b, c) in iter_primitive_pythagorean_by_perimeter(N + 1):
        p = a + b + c
        for perimeter in range(p, N + 1, p):
            solns[perimeter] += 1

    return solns.index(max(solns))
