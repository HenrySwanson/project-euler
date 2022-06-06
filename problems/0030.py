"""
Surprisingly there are only three numbers that can be written as the sum of fourth powers of their digits:

    1634 = 1^4 + 6^4 + 3^4 + 4^4
    8208 = 8^4 + 2^4 + 0^4 + 8^4
    9474 = 9^4 + 4^4 + 7^4 + 4^4

As 1 = 1^4 is not a sum it is not included.

The sum of these numbers is 1634 + 8208 + 9474 = 19316.

Find the sum of all the numbers that can be written as the sum of fifth powers of their digits.
"""

from typing import List

N = 5

# we only need to investigate 6-digit numbers (see below)
LIMIT = 6


def solve_problem() -> int:
    # We can check all possible tuples, but we can cut off some branches early
    # If we fix the first few digits, we can put bounds on both sides of the equation,
    # and if these bounds don't overlap, then we know there are no solutions with that prefix.

    # We can also do that to understand how many digits we have to look at.
    # the smallest 7-digit number is less than 7 * 9^5 = 413343, so there are no 7-digit solutions

    # We also don't actually have to track the whole list, this can be done with integers only
    # if we really want to tighten up performance
    total = 0

    def helper(remaining_digits: int, lhs_so_far: int, rhs_so_far: int) -> None:
        if remaining_digits == 0:
            if lhs_so_far == rhs_so_far:
                nonlocal total
                total += lhs_so_far
            return

        # Check whether we can prune the branch
        r = remaining_digits
        lhs_lower = lhs_so_far * 10**r  # pad with r zeros
        lhs_upper = lhs_lower + (10**r - 1)  # most we can add is all nines
        rhs_lower = rhs_so_far  # can only go up from here
        rhs_upper = rhs_lower + r * 9**N  # most we can add is all nines

        if (lhs_lower > rhs_upper) or (rhs_lower > lhs_upper):
            return

        # Okay, now try extending by one more digit
        for d in range(10):
            helper(r - 1, lhs_so_far * 10 + d, rhs_so_far + d**N)

    helper(LIMIT, 0, 0)
    return total - 1  # remember, don't count 1
