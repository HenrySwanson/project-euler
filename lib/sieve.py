from collections import defaultdict
from typing import Iterable, List

from lib.primes import Factor


def idx_to_number(i: int) -> int:
    return 2 * i + 1


def number_to_idx(n: int) -> int:
    # assume, but don't assert, n is odd
    return n // 2


class PrimeSieve:
    # The kth element of this list contains the smallest factor of 2k+1.
    # The 0th element (corresponding to 1) should never be accessed
    contents: List[int]

    def __init__(self, limit: int) -> None:
        # limit could be even! let's make it odd
        last_idx = number_to_idx(limit | 1)
        self.contents = [idx_to_number(k) for k in range(last_idx)]

        # pyre-ignore[6]: This entry should never be accessed
        self.contents[0] = object()

        for k in range(1, last_idx):
            p = idx_to_number(k)

            # If this number is composite, skip it
            if self.contents[k] != p:
                continue

            # Mark off multiples of p, unless they've already been marked
            # with some factor.
            m = p * p
            while m < limit:
                k = number_to_idx(m)
                if self.contents[k] == m:
                    self.contents[k] = p
                m += p

    def limit(self) -> int:
        last_idx = len(self.contents)
        return idx_to_number(last_idx)

    def iter_primes(self) -> Iterable[int]:
        return iter(p for k, p in enumerate(self.contents) if idx_to_number(k) == p)

    def is_prime(self, n: int) -> bool:
        limit = self.limit()

        # Special cases
        if n < 2:
            return False
        if n == 2:
            return True

        # Check if it's in the sieve
        if n < limit:
            return self.contents[number_to_idx(n)] == n
        # If it's within the ability of the sieve to check,
        # use trial division
        if n < limit * limit:
            return not any(
                # No need to check if n == p, because we know n >= limit
                n % p == 0
                for p in self.iter_primes()
            )

        raise ValueError(f"Cannot check primality of {n}; too large")

    def factor(self, n: int) -> List[Factor]:
        assert n != 0, "0 can be factored forever"

        limit = self.limit()
        factors = defaultdict(int)

        # Check 2s first
        while n % 2 == 0:
            factors[2] += 1
            n //= 2

        # If n is larger than the sieve can handle, do some
        # trial division with known primes until we're in range
        if n >= limit:
            for p in self.iter_primes():
                while n % p == 0:
                    factors[p] += 1
                    n //= p

                if n < limit:
                    break
            else:
                raise ValueError(
                    f"Unable to continue; {n} has a prime factor at least {limit}"
                )

        # Okay, we're in range
        while 1 < n < limit:
            # Find smallest prime factor
            p = self.contents[number_to_idx(n)]
            factors[p] += 1
            n //= p

        return [Factor(prime=p, multiplicity=m) for p, m in factors.items()]
