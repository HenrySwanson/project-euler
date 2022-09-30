"""
A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by 3, and a fly, F, sits in the opposite corner. By
travelling on the surfaces of the room the shortest "straight line" distance from S to F is 10 and the path is shown
on the diagram.

(A path travelling diagonally through the faces of the cube, from one corner to the other. Does not touch any other
corners.)

However, there are up to three "shortest" path candidates for any given cuboid and the shortest route doesn't always
have integer length.

It can be shown that there are exactly 2060 distinct cuboids, ignoring rotations, with integer dimensions, up to a
maximum size of M by M by M, for which the shortest route has integer length when M = 100. This is the least value
of M for which the number of solutions first exceeds two thousand; the number of solutions when M = 99 is 1975.

Find the least value of M such that the number of solutions first exceeds one million.
"""

import itertools
from math import gcd
from typing import Iterator, Tuple

from lib.pythagorean import iter_primitive_pythagorean_by_leg


N = 1_000_000


def solve_problem() -> int:
    # For a cuboid of size A x B x C, the possible path lengths are sqrt(A^2 + (B + C)^2) and its
    # permutations.
    # The shortest one is when B*C is smaller than A*C and A*B, i.e., A is largest.
    # So we want to iterate through Pythagorean triples (a, b, c), and convert them
    # into cuboids.

    limit = 2_000

    # kth element contains the number of acceptable cuboids with largest side k
    acceptable_cuboids = [0] * limit

    # If the cuboid (A, B, C) gives the Pythagorean triple (a, b, c), then c is larger
    # than a and b, one of which is max(A, B, C).
    for (a, b, _) in iter_primitive_pythagorean_by_leg(limit):
        # How many cuboids are there that give the triple (a, b, c)?
        # Either a is split up, or b is. Do we have to worry about double-counting?
        # No! The same cuboid can not come from two different triples, because we
        # always glue the two shorter sides together.
        for k in itertools.count(1):
            if k * a >= limit:
                break
            acceptable_cuboids[k * a] += count_splits(k * a, k * b)

    # Now find the first point at which the running total is > N
    total = 0
    for (i, x) in enumerate(acceptable_cuboids):
        total += x
        if total > N:
            # Note: I don't know a priori what `limit` should be set to!
            # If we could possibly have a cuboid we missed (a right triangle
            # with side length < i), we should ragequit.
            # But I have no idea how to do that.
            return i

    raise ValueError(f"Did not go high enough! You need to increase limit")


def count_splits(long: int, split: int) -> int:
    # we want to split `split` into a + b, where neither a nor b are
    # larger than `long`.
    # also, to avoid duplicates, let's enforce a >= b.

    # return len([d for d in range(split) if 0 < d <= split - d <= long])

    # Because a >= b, a >= ceil(split / 2). And because b has to be at least 1,
    # a <= split - 1. And of course, a <= long.
    max_a = min(long, split - 1)
    min_a = (split + 1) // 2
    if max_a < min_a:
        return 0

    return max_a - min_a + 1
