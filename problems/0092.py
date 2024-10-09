"""
A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.

For example,

44 → 32 → 13 → 10 → 1 → 1
85 → 89 → 145 → 42 → 20 → 4 → 16 → 37 → 58 → 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
"""

from lib.misc import to_digits

MAX = 10_000_000
MAX_SUM_SQ = 9 * 9 * 7  # 9,999,999


def solve_problem() -> int:
    # The first step is always going to knock the answer down to something in the
    # range 1 to MAX_SUM_SQ. So let's precompute those.
    destinations = [0] * (MAX_SUM_SQ + 1)
    destinations[1] = 1
    destinations[89] = 89

    for n in range(1, MAX_SUM_SQ + 1):
        chain = []
        while True:
            ans = destinations[n]
            if ans != 0:
                # We know where this goes; mark everything in the chain.
                for m in chain:
                    if m <= len(destinations):
                        destinations[m] = ans
                break

            # Otherwise, follow the chain
            chain.append(n)
            n = next_link(n)

    for i, x in enumerate(destinations):
        assert i == 0 or x != 0

    # Now churn though everything < 10M
    return sum(1 for n in range(1, MAX) if destinations[next_link(n)] == 89)


def next_link(n: int) -> int:
    digits = to_digits(n)
    return sum(d * d for d in digits)
