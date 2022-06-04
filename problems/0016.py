"""
2^15 = 32768 and the sum of its digits is 3 + 2 + 7 + 6 + 8 = 26.

What is the sum of the digits of the number 2^1000?
"""

from lib.misc import digits

def solve_problem() -> int:
    # Python trivializes this one
    return sum(digits(2**1000))
