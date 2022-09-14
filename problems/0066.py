"""
Consider quadratic Diophantine equations of the form:

x^2 – Dy^2 = 1

For example, when D=13, the minimal solution in x is 649^2 – 13×180^2 = 1.

It can be assumed that there are no solutions in positive integers when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain the following:

3^2 – 2×2^2 = 1
2^2 – 3×1^2 = 1
9^2 – 5×4^2 = 1   <---
5^2 – 6×2^2 = 1
8^2 – 7×3^2 = 1

Hence, by considering minimal solutions in x for D ≤ 7, the largest x is obtained when D=5.

Find the value of D ≤ 1000 in minimal solutions of x for which the largest value of x is obtained.
"""


import itertools
from typing import Tuple
from lib.cfrac import QuadraticCFrac, nth_convergent

from lib.misc import is_perfect_square


def solve_problem() -> int:
    # Shoot, I know this is Pell's equation, and I'm pretty sure it's related to the convergents
    # for sqrt(D), but I'm on an airplane and can't check Wikipedia...
    #
    # If x^2 - Dy^2 = 1, then (x/y)^2 - D = 1/y^2, meaning x/y is a good approximation of D.
    # Seems promising.

    return max(
        iter(d for d in range(1, 1001) if not is_perfect_square(d)),
        key=lambda d: get_minimal_soln(d)[0],
    )


def get_minimal_soln(d: int) -> Tuple[int, int]:
    cfrac = QuadraticCFrac.sqrt(d)

    # Get successive convergents. First time we get something that gives a solution
    # to the equation, we stop.
    for i in itertools.count(1):
        conv = nth_convergent(cfrac.coeffs(), i)
        num = conv.numerator
        den = conv.denominator
        if num * num - d * den * den == 1:
            return num, den

    raise AssertionError("Could not find solution to Pell's equation")
