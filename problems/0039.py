"""
If p is the perimeter of a right angle triangle with integral length sides, {a,b,c}, there are exactly three solutions for p = 120.
{20,48,52}, {24,45,51}, {30,40,50}
For which value of p ≤ 1000, is the number of solutions maximised?
"""

from cmath import sqrt
from math import ceil


N = 1000


def solve_problem() -> int:
    # We'll iterate over Pythagorean triples with sum <= N.
    # The individual legs can't be more than N/2
    solns = [0 for _ in range(N + 1)]
    for a in range(1, N // 2 + 1):
        for b in range(1, N // 2 + 1):
            c_float = sqrt(a * a + b * b)
            c = int(c_float.real)
            if c != c_float:
                continue

            if a + b + c > N:
                continue

            solns[a + b + c] += 1

    return solns.index(max(solns))
