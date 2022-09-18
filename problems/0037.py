"""
The number 3797 has an interesting property. Being prime itself, it is possible to continuously remove digits from left to right,
and remain prime at each stage: 3797, 797, 97, and 7. Similarly we can work from right to left: 3797, 379, 37, and 3.

Find the sum of the only eleven primes that are both truncatable from left to right and right to left.

NOTE: 2, 3, 5, and 7 are not considered to be truncatable primes.
"""


from typing import Iterator
from lib.misc import from_digits, to_digits
from lib.prime_state import PrimeCache


def solve_problem() -> int:
    # Each prefix of a truncatable prime must be a right-truncatable prime, and
    # # vice versa for suffixes.
    # I'm not sure how to do this without assuming that there's a finite number
    # of left- (or right-) truncatable primes...
    # Right-truncatable seems more restricted because it means our digits are restricted
    # i.e, after the first digit we can only ever use 1, 3, 7, 9
    pc = PrimeCache()

    bitruncatable = [
        p
        for d in range(10)
        for p in gen_right_truncatable_primes(pc, d)
        if is_left_truncatable(pc, p)
    ]

    return sum(bitruncatable) - 2 - 3 - 5 - 7


def gen_right_truncatable_primes(pc: PrimeCache, n: int) -> Iterator[int]:
    if pc.is_prime(n):
        yield n
    else:
        return

    # Try extending by other digits
    for d in [1, 3, 7, 9]:
        yield from gen_right_truncatable_primes(pc, 10 * n + d)


def is_left_truncatable(pc: PrimeCache, n: int) -> bool:
    digits = to_digits(n)
    return all(pc.is_prime(from_digits(digits[i:])) for i in range(len(digits)))
