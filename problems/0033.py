"""
The fraction 49/98 is a curious fraction, as an inexperienced mathematician in attempting to simplify it may incorrectly believe that 49/98 = 4/8, which is correct, is obtained by cancelling the 9s.

We shall consider fractions like, 30/50 = 3/5, to be trivial examples.

There are exactly four non-trivial examples of this type of fraction, less than one in value, and containing two digits in the numerator and denominator.

If the product of these four fractions is given in its lowest common terms, find the value of the denominator.
"""

from itertools import product
from math import prod
import math
from typing import List, Tuple


def solve_problem() -> int:
    # Let's just write it as ab/cd and try all 10^4 pairs
    fractions = [
        frac
        for t in product(range(10), repeat=3)
        for frac in gen_curious(*t)
        if frac[0] < frac[1] and frac[0] >= 10
    ]

    num = prod(num for (num, den) in fractions)
    den = prod(den for (num, den) in fractions)
    gcd = math.gcd(num, den)
    return den // gcd


def gen_curious(a: int, b: int, c: int) -> List[Tuple[int, int, int]]:
    results = []
    ac = 10 * a + c
    bc = 10 * b + c
    ca = 10 * c + a
    cb = 10 * c + b
    # ac/bc = a/b
    if c != 0 and ac * b == a * bc:
        results.append((ac, bc))
    # ac/cb = a/b
    if ac * b == a * cb:
        results.append((ac, cb))
    # ca/bc = a/b
    if ca * b == a * bc:
        results.append((ca, bc))
    # ca/cb = a/b
    if c != 0 and ca * b == a * cb:
        results.append((ca, cb))
    return results
