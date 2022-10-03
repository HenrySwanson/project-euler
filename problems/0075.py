"""
It turns out that 12 cm is the smallest length of wire that can be bent to form an integer sided right angle
triangle in exactly one way, but there are many more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form an integer sided right angle triangle,
and other lengths allow more than one solution to be found; for example, using 120 cm it is possible to form
exactly three different integer sided right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L ≤ 1,500,000 can exactly one integer sided
right angle triangle be formed?
"""

from collections import defaultdict
from math import gcd, sqrt

from lib.pythagorean import iter_primitive_pythagorean_by_perimeter


N = 1_500_000


def solve_problem() -> int:
    # N is too large to do this naively, so let's be smarter.
    # All primitive Pythagorean triples can be uniquely parameterized as:
    #   (m^2 - n^2) / 2, mn, (m^2 + n^2) / 2, with m > n, m and n coprime and odd
    # Multiplying by k gives all triples (uniquely)

    # The perimeter of such a triangle is then: km^2 + kmn = km(m + n).
    # I tried to do something with factoring, but it's very tricky. So we'll
    # just iterate all relevant (k, m, n) pairs.

    counter = defaultdict(int)

    for (a, b, c) in iter_primitive_pythagorean_by_perimeter(N + 1):
        prim_perimeter = a + b + c

        for perimeter in range(prim_perimeter, N + 1, prim_perimeter):
            counter[perimeter] += 1

    return sum(1 for size in counter.values() if size == 1)
