"""
The cube, 41063625 (345^3), can be permuted to produce two other cubes:
56623104 (384^3) and 66430125 (405^3).
In fact, 41063625 is the smallest cube which has exactly three permutations
of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits
are cube.
"""


from collections import defaultdict
import itertools
from lib.misc import from_digits, increasing_seq_cache, increasing_seq_cutoff, to_digits

N = 5


def solve_problem() -> int:
    is_cube = increasing_seq_cache(lambda x: x * x * x)

    for k in itertools.count(1):
        # Generate all cubes of k digits
        cubes = increasing_seq_cutoff(lambda x: x * x * x, 10 ** (k - 1), 10**k)

        buckets = defaultdict(list)
        for cube in cubes:
            key = tuple(sorted(to_digits(cube)))
            buckets[key].append(cube)

        # Check if we've got any buckets of the right size. If so, take the
        # minimum across all of them
        answers = [
            cube
            for (key, cubes) in buckets.items()
            for cube in cubes
            if len(cubes) == N
        ]

        if answers:
            return min(answers)

    for n in itertools.count(0):
        cube = n * n * n
        digits = to_digits(cube)

        num_cubes = sum(
            1 for perm in itertools.permutations(digits) if is_cube(from_digits(perm))
        )

        if n == 345:
            print(
                list(
                    from_digits(perm)
                    for perm in itertools.permutations(digits)
                    if is_cube(from_digits(perm))
                )
            )

        if num_cubes == N:
            return cube

    raise AssertionError()
