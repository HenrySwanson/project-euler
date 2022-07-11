"""
It is possible to show that the square root of two can be expressed as an infinite continued fraction.

sqrt(2) = 1 + 1/(2 + 1/(2 + 1/(2 + ...)))

By expanding this for the first four iterations, we get:

1 + 1/2 = 3/2 = 1.5
1 + 1/(2 + 1/2) = 7/5 = 1.4
1 + 1/(2 + 1/(2 + 1/2)) = 17/12 = 1.41666...
1 + 1/1 + 1/(2 + 1/(2 + 1/(2 + 1/2))) = 41/29 = 1.41379...

The next three expansions are 99/70, 239/169, and 577/408, but the eighth expansion, 1393/985, is the first example
where the number of digits in the numerator exceeds the number of digits in the denominator.

In the first one-thousand expansions, how many fractions contain a numerator with more digits than the denominator?
"""


from lib.misc import num_digits

N = 1000


def solve_problem() -> int:
    # If some expansion is a/b, then the next is 1 + 1/(1 + a/b) = (a+2b)/(a+b)
    num = 3
    den = 2
    total = 0
    # Already did the first one
    for _ in range(2, N):
        num, den = (num + 2 * den), (num + den)
        if num_digits(num) > num_digits(den):
            total += 1
    return total
