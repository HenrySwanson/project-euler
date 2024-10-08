"""
Each of the six faces on a cube has a different digit (0 to 9) written on it; the same is done to a second cube. By placing the two cubes side-by-side in different positions we can form a variety of 2-digit numbers.

For example, the square number 64 could be formed:

<image>

In fact, by carefully choosing the digits on both cubes it is possible to display all of the square numbers below one-hundred: 01, 04, 09, 16, 25, 36, 49, 64, and 81.

For example, one way this can be achieved is by placing {0, 5, 6, 7, 8, 9} on one cube and {1, 2, 3, 4, 8, 9} on the other cube.

However, for this problem we shall allow the 6 or 9 to be turned upside-down so that an arrangement like {0, 5, 6, 7, 8, 9} and {1, 2, 3, 4, 6, 7} allows for all nine square numbers to be displayed; otherwise it would be impossible to obtain 09.

In determining a distinct arrangement we are interested in the digits on each cube, not the order.

{1, 2, 3, 4, 5, 6} is equivalent to {3, 6, 4, 1, 2, 5}
{1, 2, 3, 4, 5, 6} is distinct from {1, 2, 3, 4, 5, 9}

But because we are allowing 6 and 9 to be reversed, the two distinct sets in the last example both represent the extended set {1, 2, 3, 4, 5, 6, 9} for the purpose of forming 2-digit numbers.

How many distinct arrangements of the two cubes allow for all of the square numbers to be displayed?
"""

from itertools import combinations
from typing import List


def rotate_digit(n: int) -> int:
    if n == 9:
        return 6
    return n


SQUARES = [x * x for x in range(1, 10)]
SQUARE_DIGITS = [(rotate_digit(x // 10), rotate_digit(x % 10)) for x in SQUARES]


def solve_problem() -> int:
    # only 10 choose 6 = 210 combinations, pretty small!
    cubes = list(combinations([0, 1, 2, 3, 4, 5, 6, 7, 8, 6], 6))
    return sum(
        1 for idx, c1 in enumerate(cubes) for c2 in cubes[idx:] if is_correct(c1, c2)
    )


def is_correct(cube_a: List[int], cube_b: List[int]) -> bool:
    for x, y in SQUARE_DIGITS:
        if not can_spell(cube_a, cube_b, x, y):
            return False
    return True


def can_spell(cube_a: List[int], cube_b: List[int], d1: int, d2: int) -> bool:
    # Check that it's spellable as AB or BA or both
    ab = d1 in cube_a and d2 in cube_b
    ba = d1 in cube_b and d2 in cube_a
    return ab or ba
