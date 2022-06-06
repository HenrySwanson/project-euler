"""
Starting with the number 1 and moving to the right in a clockwise direction a 5 by 5 spiral is formed as follows:

21 22 23 24 25
20  7  8  9 10
19  6  1  2 11
18  5  4  3 12
17 16 15 14 13

It can be verified that the sum of the numbers on the diagonals is 101.

What is the sum of the numbers on the diagonals in a 1001 by 1001 spiral formed in the same way?
"""

from lib.misc import sum_of_n_squares, triangle


N = 1001


def solve_problem() -> int:
    # This is a math-only problem

    # The last element in each ring is an odd square (1, 9, 25), and it's always in the corner.
    # So the kth ring is the numbers from (2k-1)^2 + 1 to (2k+1)^2, inclusive. That ring has
    # size 8k.

    # The numbers in the corners are then therefore:
    #   X + (X - 2k) + (X - 4k) + (X - 6k) = 4X - 12k
    # where X = (2k+1)^2, which is:
    #   4X + 12k = 16k^2 + 4k + 4

    # Finally, we want to sum over the first K rings:
    #   sum (k <= K) 16k^2 + 4k + 4
    # = 16 [K(K+1)(2K+1)] / 6 + 4 [K(K+1)] / 2 + 4K

    # Then add 1 for the center

    K = (N - 1) // 2
    return 16 * sum_of_n_squares(K) + 4 * triangle(K) + 4 * K + 1
