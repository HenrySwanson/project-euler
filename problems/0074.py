"""
The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:

1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169; it turns out that there are only three such loops that exist:

169 → 363601 → 1454 → 169
871 → 45361 → 871
872 → 45362 → 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69 → 363600 → 1454 → 169 → 363601 (→ 1454)
78 → 45360 → 871 → 45361 (→ 871)
540 → 145 (→ 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?
"""


from math import factorial
from lib.misc import to_digits

N = 1_000_000
LIMIT = 60


def solve_problem() -> int:
    # We are kindly given the only possible loops, so let's make use of them.
    loop_sizes = {}
    for n in [1, 2, 145, 169, 871, 872]:
        loop = []
        while n not in loop:
            loop.append(n)
            n = next_step(n)
        for n in loop:
            loop_sizes[n] = len(loop)

    cache = dict(loop_sizes)

    def solve(n: int) -> None:
        if n in cache:
            return cache[n]
        # We were given the only possible _non-singleton_ loops, so we have to watch out for
        # the singletons.
        n2 = next_step(n)
        if n == n2:
            value = 1
        else:
            value = 1 + solve(n2)
        cache[n] = value
        return value

    for n in range(N):
        solve(n)

    return sum(1 for x in cache.values() if x == LIMIT)


def next_step(n: int) -> int:
    return sum(factorial(d) for d in to_digits(n))
