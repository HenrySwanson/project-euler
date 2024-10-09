"""
The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of 28 are 1, 2, 4, 7, and 14. As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220, forming a chain of two numbers. For this reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496, we form a chain of five numbers:

12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.
"""

from lib.prime_state import PrimeCache
from lib.primes import sum_divisors


MAXIMUM = 1_000_000


def solve_problem() -> int:
    visited = [False] * (MAXIMUM + 1)
    pc = PrimeCache()
    pc.init_sieve_of_eratosthenes(MAXIMUM)
    best_length = 0
    answer = 0

    # TODO: can i precompute the sum of divisors as a table?
    # no need to make a prime sieve.

    for n in range(1, MAXIMUM + 1):
        # If we've already seen this number, we know it either wasn't
        # part of a chain, or it's part of one we've already examined.
        if visited[n]:
            continue

        chain = [n]
        while True:
            # watch out: prime -> 1 -> 0
            if n == 0:
                break

            # ignore chains if they jump above a million
            if n > MAXIMUM:
                break

            # if we've already seen this one in another sequence,
            # give up, not a chain. then, mark it
            if visited[n]:
                break
            visited[n] = True

            # what's the next link in the chain?
            n = sum_divisors(pc.factor(n)) - n

            # is it a loop? remember, it may not loop from the beginning!
            if n in chain:
                idx = chain.index(n)
                loop = chain[idx:]
                if len(loop) > best_length:
                    best_length = len(loop)
                    answer = min(loop)
                break

            chain.append(n)

    return answer
