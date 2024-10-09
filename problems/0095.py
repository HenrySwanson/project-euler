"""
The proper divisors of a number are all the divisors excluding the number itself. For example, the proper divisors of 28 are 1, 2, 4, 7, and 14. As the sum of these divisors is equal to 28, we call it a perfect number.

Interestingly the sum of the proper divisors of 220 is 284 and the sum of the proper divisors of 284 is 220, forming a chain of two numbers. For this reason, 220 and 284 are called an amicable pair.

Perhaps less well known are longer chains. For example, starting with 12496, we form a chain of five numbers:

12496 → 14288 → 15472 → 14536 → 14264 (→ 12496 → ...)

Since this chain returns to its starting point, it is called an amicable chain.

Find the smallest member of the longest amicable chain with no element exceeding one million.
"""

import itertools

MAXIMUM = 1_000_000


def solve_problem() -> int:
    visited = [False] * (MAXIMUM + 1)
    best_length = 0
    answer = 0

    # Precompute a table of sum-of-divisors. This turns out to be
    # quite a bit faster than on-demand factoring every integer.
    # Takes it from 18s to 2s.

    # 1 will contribute 1 to everyone in the table, so we can
    # just bake that in at the beginning
    sum_divisors_table = [1] * (MAXIMUM + 1)
    for i in itertools.count(2):
        # on this loop, we'll mark all the n for which n = ik with k >= i
        # for k < i, we'll have marked it on a previous loop (see below)
        if i * i >= len(sum_divisors_table):
            break

        sum_divisors_table[i * i] += i
        for k in itertools.count(i + 1):
            n = i * k
            if n >= len(sum_divisors_table):
                break
            # we add the divisor i, but also, while we're at it,
            # we can add the other divisor, k. (this is why we start
            # iterating at i+1, so that k > i)
            sum_divisors_table[n] += i + k

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
            n = sum_divisors_table[n]

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
