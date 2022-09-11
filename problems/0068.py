"""
Consider the following "magic" 3-gon ring, filled with the numbers 1 to 6, and each line adding to nine.

  4
   \
    3
   / \
  1 - 2 - 6
 /
5

Working clockwise, and starting from the group of three with the numerically lowest external node
(4,3,2 in this example), each solution can be described uniquely. For example, the above solution
can be described by the set: 4,3,2; 6,2,1; 5,1,3.

It is possible to complete the ring with four different totals: 9, 10, 11, and 12.
There are eight solutions in total.

Total    Solution Set
9    4,2,3; 5,3,1; 6,1,2
9    4,3,2; 6,2,1; 5,1,3
10    2,3,5; 4,5,1; 6,1,3
10    2,5,3; 6,3,1; 4,1,5
11    1,4,6; 3,6,2; 5,2,4
11    1,6,4; 5,4,2; 3,2,6
12    1,5,6; 2,6,4; 3,4,5
12    1,6,5; 3,5,4; 2,4,6

By concatenating each group it is possible to form 9-digit strings; the maximum string
for a 3-gon ring is 432621513.

Using the numbers 1 to 10, and depending on arrangements, it is possible to form
16- and 17-digit strings. What is the maximum 16-digit string for a "magic" 5-gon ring?

(same kind of shape as above but with 5-fold symmetry)
"""


import itertools
from typing import Iterator, List, Sequence, Set, Tuple

from lib.misc import from_digits, num_digits, to_digits

N = 5


def solve_problem() -> int:
    # We'll try to fill in nearby circles as much as possible, so I'm labeling them
    # in the order of: inner, outer, opposite inner, etc.
    # So the straight lines are: 1, 2, 3; 3, 5, 7, ...
    # Well, because 0-indexing, it's 0, 1, 2; 2, 3, 4, ...
    #
    # So if it were 4-fold symmetry it'd be
    #     3
    # 1 0 2
    #   6 4 5
    #   7

    straight_lines: List[List[int]] = [
        [(2 * k + x) % (2 * N) for x in [1, 0, 2]] for k in range(N)
    ]

    def get_value(solution: Sequence[int]) -> int:
        # print(
        #     "; ".join(
        #         ", ".join([str(solution[i]) for i in line]) for line in straight_lines
        #     )
        # )

        chunks = [solution[i] for line in straight_lines for i in line]
        return from_digits([d for n in chunks for d in to_digits(n)])

    return max(x for soln in initial_phase() if num_digits(x := get_value(soln)) == 16)


def initial_phase() -> Iterator[Tuple[int, ...]]:
    # First, we set numbers on the first line.
    # This will determine what the magic sum must be.
    numbers = set(range(1, 2 * N + 1))
    # Constraint 0+1+2 is always satisfied
    for triple in itertools.permutations(numbers, 3):
        magic_sum = sum(triple)
        remaining = numbers - set(triple)

        yield from middle_phase(triple, remaining, magic_sum)


def middle_phase(
    slots: Tuple[int, ...], remaining: Set[int], magic_sum: int
) -> Iterator[Tuple[int, ...]]:
    # Then we try placing numbers on the adjacent line. If it matches
    # the sum, great, continue. Otherwise try other numbers.
    last = slots[-1]
    for pair in itertools.permutations(remaining, 2):
        if last + pair[0] + pair[1] != magic_sum:
            continue

        # Optimization: we don't want to double-count patterns that
        # are rotations of each other. So we insist that slot[1] is
        # the smallest of its conjugates.
        if pair[0] < slots[1]:
            continue

        new_slots = slots + pair
        new_remaining = remaining - set(pair)
        if len(new_remaining) > 1:
            yield from middle_phase(new_slots, new_remaining, magic_sum)
        else:
            yield from final_phase(new_slots, new_remaining.pop(), magic_sum)


def final_phase(
    slots: Tuple[int, ...], final: int, magic_sum: int
) -> Iterator[Tuple[int, ...]]:
    # We're left with one number, does this work?
    last = slots[-1]
    first = slots[0]

    # Again, skip if this isn't the canonical rotation
    if final < slots[1]:
        return

    if first + last + final == magic_sum:
        new_slots = slots + (final,)
        yield new_slots
