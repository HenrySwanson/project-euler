import dataclasses
import math
from typing import Iterator, List

# Some global state for caching primes
_PRIMES: List[int] = [2]
_NEXT_INTEGER_TO_CHECK: int = 3


@dataclasses.dataclass
class Factor:
    prime: int
    multiplicity: int


def iter_primes() -> Iterator[int]:
    # TODO: is there any chicanery that can occur if we have two of these iterators
    # going at once? probably...

    global _NEXT_INTEGER_TO_CHECK

    # Helper fn that checks against the list of known primes.
    # Assumes that _PRIMES is sorted and that n is not much higher than _PRIMES[-1]
    def test(n: int) -> bool:
        for p in _PRIMES:
            if n % p == 0:
                return False
            if p * p > n:
                break
        return True

    for p in _PRIMES:
        yield p

    while True:
        n = _NEXT_INTEGER_TO_CHECK
        # Check if n is prime, and if so, yield it
        if test(n):
            yield n
            _PRIMES.append(n)

        # In any case, bump n
        _NEXT_INTEGER_TO_CHECK += 2


def factor(n: int) -> Iterator[Factor]:
    assert n != 0, "0 can be factored forever"

    for p in iter_primes():
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
