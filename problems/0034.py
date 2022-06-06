"""
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the factorial of their digits.

Note: As 1! = 1 and 2! = 2 are not sums they are not included.
"""


from math import factorial
from typing import Iterator


def solve_problem() -> int:
    # Well, I have to bound something here...
    # 9! is six-digits, so I think that checking all 7-digits numbers is
    # sufficient, similar to problem 30.
    # Maybe we can do it bottom up this time though?
    # Actually yeah, that's pretty nice. Generators are sweet.
    return sum(x for x in explore(0, 0, 0, True) if x > 10)


def explore(n: int, k: int, sum_so_far: int, leading_zero: bool) -> Iterator[int]:
    # We have a k-digit number n (<= 10^k), whose sum of factorials of digits is sum_so_far.
    # If n == sum_so_far, yield it.
    #
    # We will try prepending a new digit to the start of the number, and recurse, but first,
    # if we can tell that recursion would be fruitless, bail out.
    if n == sum_so_far and not leading_zero:
        yield n

    ten_power_k = 10**k
    # if there's no chance that sum_so_far can ever catch up, abort
    if n + ten_power_k > sum_so_far + factorial(9):
        return

    for d in range(10):
        yield from explore(
            n + ten_power_k * d, k + 1, sum_so_far + factorial(d), d == 0
        )
