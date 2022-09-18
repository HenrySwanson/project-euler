"""
Let d(n) be defined as the sum of proper divisors of n (numbers less than n which divide evenly into n).
If d(a) = b and d(b) = a, where a ≠ b, then a and b are an amicable pair and each of a and b are called amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20, 22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284 are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""

from lib.prime_state import PrimeCache
from lib.primes import sum_divisors


def solve_problem() -> int:
    return sum(x for x in range(1, 10001) if is_amicable(x))


def is_amicable(x: int) -> bool:
    pc = PrimeCache()
    y = sum_divisors(pc.factor(x)) - x
    if x == y or y == 0:
        return False
    return x == sum_divisors(pc.factor(y)) - y
