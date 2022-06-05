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
    total = 0
    def helper(seq: List[int]) -> None:
        if len(seq) == LIMIT:
            if lhs(seq) == rhs(seq):
                nonlocal total
                total += lhs(seq)
            return

        seq.append(0)
        remaining = LIMIT - len(seq)
        for d in range(10):
            seq[-1] = d
            lhs_lower = lhs(seq)
            lhs_upper = lhs_lower + (10**remaining - 1)  # most we can add is all nines
            rhs_lower = rhs(seq)
            rhs_upper = rhs_lower + remaining * 9**N  # most we can add is all nines
            if (lhs_lower > rhs_upper) or (rhs_lower > lhs_upper):
                continue
            helper(seq)
        seq.pop()

    helper([])
    return total - 1  # remember, don't count 1

def lhs(seq: List[int]) -> int:
    return sum(
        a * 10**(LIMIT - k - 1) for (k, a) in enumerate(seq)
    )

def rhs(seq: List[int]) -> int:
    return sum(a**N for a in seq)