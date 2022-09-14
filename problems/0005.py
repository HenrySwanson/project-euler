"""
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.

What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
"""

import math


def solve_problem() -> int:
    # I think this is the first one where brute force doesn't work.

    # Iteratively compute LCMs
    answer = 1
    for k in range(1, 21):
        answer = math.lcm(answer, k)
    return answer
