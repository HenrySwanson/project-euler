from bisect import bisect_left
import dataclasses
from typing import Iterator, List

# Some private state used for caching info about primes
@dataclasses.dataclass
class PrimeCache:
    primes: List[int] = dataclasses.field(default_factory=lambda: [2])
    next_to_check: int = 3

    def clear(self) -> None:
        self.primes = [2]
        self.next_to_check = 3

    def init_sieve_of_eratosthenes(self, limit: int) -> None:
        # Skip if we don't need it
        if limit <= self.next_to_check:
            return

        # TODO: re-use partial knowledge of primes?
        sieve = [True for _ in range(limit)]
        sieve[0] = sieve[1] = False
        for p in range(limit):
            # If this number has been marked off, skip it
            if not sieve[p]:
                continue
            # If p^2 >= n, then we're done
            if p * p >= limit:
                break
            # Otherwise, start marking off multiples of p, starting at p^2
            k = p
            while p * k < limit:
                sieve[p * k] = False
                k += 1

        self.primes = [p for (p, is_prime) in enumerate(sieve) if is_prime]
        # some care here -- ensure that it's odd
        self.next_to_check = limit | 1

    def iter_primes(self) -> Iterator[int]:
        for p in self.primes:
            yield p

        yield from self._iter_primes_from_end()

    def _iter_primes_from_end(self) -> Iterator[int]:
        # TODO: is there any chicanery that can occur if we have two of these iterators
        # going at once? probably...

        while True:
            n = self.next_to_check

            # Check if n is prime, and if so, yield it
            if self._test_against_known_primes(n):
                yield n
                self.primes.append(n)

            # In any case, bump n
            self.next_to_check += 2

    def _test_against_known_primes(self, n: int) -> bool:
        if n < 2:
            return False

        assert n < self.primes[-1] * self.primes[-1]
        for p in self.primes:
            if n % p == 0:
                return False
            if p * p > n:
                break
        return True

    def is_prime(self, n: int) -> bool:
        if n < self.next_to_check:
            idx = bisect_left(self.primes, n)
            return idx < len(self.primes) and self.primes[idx] == n

        # TODO: is it cheaper to try factoring instead, because of the sqrt bound?
        for p in self._iter_primes_from_end():
            if p == n:
                return True
            if p > n:
                return False

        raise AssertionError()
