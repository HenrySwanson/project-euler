import dataclasses
import math
from typing import Iterator, Optional

from lib.prime_state import PrimeCache

# Some global state, don't worry about it
_PRIME_STATE = PrimeCache()


@dataclasses.dataclass
class Factor:
    prime: int
    multiplicity: int


def is_prime(n: int) -> bool:
    return _PRIME_STATE.is_prime(n)


def iter_primes(cutoff: Optional[int] = None) -> Iterator[int]:
    if cutoff is not None:
        _PRIME_STATE.init_sieve_of_eratosthenes(cutoff)

    for p in _PRIME_STATE.iter_primes():
        if cutoff is not None and p >= cutoff:
            return
        yield p


def init_primes_up_to(cutoff: int) -> None:
    _PRIME_STATE.init_sieve_of_eratosthenes(cutoff)


def factor(n: int) -> Iterator[Factor]:
    assert n != 0, "0 can be factored forever"

    for p in _PRIME_STATE.iter_primes():
        multiplicity = 0
        while n % p == 0:
            multiplicity += 1
            n //= p
        if multiplicity > 0:
            yield Factor(prime=p, multiplicity=multiplicity)

        if p * p > n:
            break

    # Account for the final remaining prime factor
    if n != 1:
        yield Factor(prime=n, multiplicity=1)


def num_divisors(n: int) -> int:
    # Number of divisors is prod(k+1) where n = prod p^k
    return math.prod(f.multiplicity + 1 for f in factor(n))


def sum_divisors(n: int) -> int:
    # Sum of divisors is prod(1 + p + ... + p^k) where n = prod(p^k)
    # Equivalently, (p^(k+1) - 1)/(p-1)
    result = 1
    return math.prod(
        (f.prime ** (f.multiplicity + 1) - 1) // (f.prime - 1) for f in factor(n)
    )
