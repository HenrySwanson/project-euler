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

from typing import List

# Put 7 last because it's the only digit we don't use,
# and put 6 and 9 near the end because they're strange.
DIGITS = [0, 1, 2, 3, 4, 5, 8, 6, 9, 7]

SQUARES = [x * x for x in range(1, 10)]
SQUARE_DIGITS = [(x // 10, x % 10) for x in SQUARES]
SQUARE_MAP = {
    x: [
        y
        for y in range(10)
        if x >= y and ((x,y) in SQUARES or (y, x) in SQUARES)
    ]
    for x in range(10)
}


def solve_problem() -> int:
    return foo([], [], 0)

def foo(cube_a: List[int], cube_b: List[int], idx: int) -> int:
    # Are we at the end of the digit list? If so, our cubes are nearly
    # complete.
    if idx == len(DIGITS):
        if is_correct(cube_a, cube_b):
            # Deduplicate
            if tuple(cube_a) <= tuple(cube_b):
                return 1
        return 0

    # We try placing the number on one cube, the other cube, both, or
    # neither.
    total = 0
    digit = DIGITS[idx]

    # Neither cube
    if is_viable(cube_a, cube_b, hint=digit):
        total += foo(cube_a, cube_b, idx + 1)

    # Just on cube A
    cube_a.append(digit)
    if is_viable(cube_a, cube_b, hint=digit):
        total += foo(cube_a, cube_b, idx + 1)

    # On both cubes
    cube_b.append(digit)
    if is_viable(cube_a, cube_b, hint=digit):
        total += foo(cube_a, cube_b, idx + 1)

    # Only on cube B
    cube_a.pop()
    if is_viable(cube_a, cube_b, hint=digit):
        total += foo(cube_a, cube_b, idx + 1)

    # Restore cubes to original state
    cube_b.pop()
    return total


def is_viable(cube_a: List[int], cube_b: List[int], hint: int) -> bool:
    # First, are both cubes <= 6 sides?
    if len(cube_a) > 6 or len(cube_b) > 6:
        return False

    # 6s and 9s are weird, just optimistically say yes.
    # (Why? Because we get a 'second chance' to spell squares with 6s and 9s. Just
    # because we can't spell it now doesn't mean we can't spell it later.)
    if hint == 6 or hint == 9:
        return True
    
    # Next, check that it's possible to spell the desired squares with these
    # cubes. Previous calls to is_viable have checked other squares, so we
    # only check those where the biggest digit is `hint`.
    for d in SQUARE_MAP[hint]:
        if not can_spell(cube_a, cube_b, d, hint):
            return False

    return True

def is_correct(cube_a: List[int], cube_b: List[int]) -> bool:
    if len(cube_a) != 6 or len(cube_b) != 6:
        return False

    for (x, y) in SQUARE_DIGITS:
        if not can_spell(cube_a, cube_b, x, y):
            return False
    return True

def can_spell(cube_a: List[int], cube_b: List[int], d1: int, d2: int) -> bool:
    # Check that it's spellable as AB or BA or both
    ab = has_digit_or_69(cube_a, d1) and has_digit_or_69(cube_b, d2)
    ba = has_digit_or_69(cube_b, d1) and has_digit_or_69(cube_a, d2)
    return ab or ba

def has_digit_or_69(cube: List[int], digit: int) -> bool:
    if digit == 6 or digit == 9:
        return 6 in cube or 9 in cube
    return digit in cube