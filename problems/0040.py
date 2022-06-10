"""
An irrational decimal fraction is created by concatenating the positive integers:
0.12345678910*1*112131415161718192021...
It can be seen that the 12^th digit of the fractional part is 1.
If d_n represents the n^th digit of the fractional part, find the value of the following expression.
d_1 × d_10 × d_100 × d_1000 × d_10000 × d_100000 × d_1000000
"""


from math import prod
from lib.misc import to_digits


def solve_problem() -> int:
    return prod(d(10**k) for k in range(6))


def d(n: int) -> int:
    # The first 9 digits are 1-9
    # The next 90*2 digits are 10-99
    # The next 900*3 digits are 100-999
    #
    # So if n < 10, we just return n
    # Otherwise, subtract off the length of the 1-digit range (10), and
    # check if we're within the 2-digit range (90*2 digits).
    # If so, done, else, subtract off the length of that range (90*2), and
    # check if we're within the 3-digit range (900*3 digits).
    # Repeat

    # But first, correct for 1-indexing
    assert n >= 1
    n -= 1

    k = 1  # digit range: 1 means 1-9, 2 means 10-99
    ten_power = 1  # 10^(k-1)
    while n >= 9 * ten_power * k:
        n -= 9 * ten_power * k
        k += 1
        ten_power *= 10

    # We know can find which number we're associated with, and how far
    # into the number we need to index
    number = n // k + ten_power
    idx = n % k
    return list(to_digits(number))[idx]
