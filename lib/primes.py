import dataclasses
import math
from typing import Iterable


@dataclasses.dataclass(eq=True, order=True)
class Factor:
    prime: int
    multiplicity: int


def num_distinct_prime_factors(factors: Iterable[Factor]) -> int:
    return sum(1 for _ in factors)


def num_divisors(factors: Iterable[Factor]) -> int:
    # Number of divisors is prod(k+1) where n = prod p^k
    return math.prod(f.multiplicity + 1 for f in factors)


def sum_divisors(factors: Iterable[Factor]) -> int:
    # Sum of divisors is prod(1 + p + ... + p^k) where n = prod(p^k)
    # Equivalently, (p^(k+1) - 1)/(p-1)
    return math.prod(
        (f.prime ** (f.multiplicity + 1) - 1) // (f.prime - 1) for f in factors
    )


def totient(n: int, factors: Iterable[Factor]) -> int:
    # n * prod (1 - 1/p)
    factors = list(factors)
    num = math.prod(f.prime - 1 for f in factors)
    den = math.prod(f.prime for f in factors)
    return n * num // den
