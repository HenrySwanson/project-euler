"""
The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28.
In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 2^2 + 2^3 + 2^4
33 = 3^2 + 2^3 + 2^4
49 = 5^2 + 2^3 + 2^4
47 = 2^2 + 3^3 + 2^4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and
prime fourth power?
"""


from math import sqrt
from lib.prime_state import PrimeCache

N = 50_000_000


def solve_problem() -> int:
    pc = PrimeCache()
    pc.init_sieve_of_eratosthenes(int(sqrt(N)))

    numbers = set()
    for p in pc.iter_primes():
        p2 = p * p
        bound = N - p2
        if bound < 0:
            break

        for q in pc.iter_primes():
            q3 = q * q * q
            inner_bound = bound - q3
            if inner_bound < 0:
                break

            for r in pc.iter_primes():
                r4 = r * r * r * r
                n = p2 + q3 + r4
                if n > N:
                    break
                numbers.add(n)

    return len(numbers)
