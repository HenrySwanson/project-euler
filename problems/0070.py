"""
Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine
the number of positive numbers less than or equal to n which are relatively prime to n.
For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to
nine, φ(9)=6.

The number 1 is considered to be relatively prime to every positive number, so φ(1)=1. 

Interestingly, φ(87109)=79180, and it can be seen that 87109 is a permutation of 79180.

Find the value of n, 1 < n < 10^7, for which φ(n) is a permutation of n and
the ratio n/φ(n) produces a minimum.
"""

from lib.misc import to_digits
from lib.primes import init_primes_up_to, totient


N = 10_000_000

def solve_problem() -> int:
    init_primes_up_to(N)
    
    candidates = [
        n for n in range(2, N) if same_digits(n, totient(n))
    ]

    return min(candidates, key = lambda n: n/totient(n))

def same_digits(a: int, b: int) -> bool:
    return sorted(to_digits(a)) == sorted(to_digits(b))

# TODO: this is incredibly slow
# instead of iterating through the numbers from 1 -> N, we should
# iterate by their prime decomposition; minimizing n/phin is
# naturally done that way

# the best case scenario is one prime, but that's non-palindromic
# so try two primes

# TODO: prove best case scenario is two primes of equalish size
# (like how rectangle areas work). then we can rule out 3 primes after we
# find a solution with 2 primes?