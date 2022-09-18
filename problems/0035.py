"""
The number, 197, is called a circular prime because all rotations of the digits: 197, 971, and 719, are themselves prime.

There are thirteen such primes below 100: 2, 3, 5, 7, 11, 13, 17, 31, 37, 71, 73, 79, and 97.

How many circular primes are there below one million?
"""


import itertools
from typing import List
from lib.prime_state import PrimeCache
from lib.misc import from_digits


def solve_problem() -> int:
    pc = PrimeCache()

    count = sum(
        1
        for k in range(2, 7)
        for ds in itertools.product([1, 3, 7, 9], repeat=k)
        if is_circular(pc, ds)
    )
    return count + 4  # for 2, 3, 5, 7


def is_circular(pc: PrimeCache, ds: List[int]) -> bool:
    return all(pc.is_prime(from_digits(ds[i:] + ds[:i])) for i in range(len(ds)))
