"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once. For example, 2143 is a 4-digit pandigital and is also prime.
What is the largest n-digit pandigital prime that exists?
"""


from itertools import permutations
from lib.primes import init_primes_up_to, is_prime
from lib.misc import from_digits


def solve_problem() -> int:
    # Well, we know that it can't use 1-9, because then it'd be divisible by 9.
    # Same with 1-8. So we'll look for 1-7, i.e., an upper bound of 7654321.
    # Sqrt of that is <9000.
    init_primes_up_to(9000)

    # Let's start from the top so we can end quickly!
    # Don't know why I didn't think about that for other problems...
    for digits in permutations(reversed(range(1, 8))):
        n = from_digits(digits)
        if is_prime(n):
            return n

    raise AssertionError()
