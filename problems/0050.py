"""
The prime 41, can be written as the sum of six consecutive primes:
41 = 2 + 3 + 5 + 7 + 11 + 13
This is the longest sum of consecutive primes that adds to a prime below one-hundred.
The longest sum of consecutive primes below one-thousand that adds to a prime, contains 21 terms, and is equal to 953.
Which prime, below one-million, can be written as the sum of the most consecutive primes?
"""


from lib.prime_state import PrimeCache

N = 1_000_000


def solve_problem() -> int:
    pc = PrimeCache()

    # First, generate all primes up to N, because we don't need more
    primes = list(pc.iter_primes(cutoff=N))

    # Then find out what sequence length is reasonable to start with. If
    # the initial segment of length k sums to > N, we don't need to consider runs
    # of length k or more.
    max_len = len(primes)
    for k in range(len(primes)):
        max_len = k
        if sum(primes[:k]) > N:
            break

    # Now, we sum over windows of length k, k-1, k-2, ... until we find a prime
    for n in reversed(range(max_len)):
        for k in range(len(primes) - n):
            s = sum(primes[k : k + n])

            # Okay, no sense exploring things higher than a million
            if s >= N:
                break

            if pc.is_prime(s):
                return s

    raise AssertionError()
