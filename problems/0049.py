"""
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms increases by 3330,
is unusual in two ways: (i) each of the three terms are prime, and, (ii) each of the 4-digit
numbers are permutations of one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit primes, exhibiting this property,
but there is one other 4-digit increasing sequence.

What 12-digit number do you form by concatenating the three terms in this sequence?
"""


from lib.misc import from_digits, to_digits
from lib.primes import is_prime, iter_primes


def solve_problem() -> int:
    four_digit_primes = [p for p in iter_primes(cutoff=10_000) if p >= 1000]
    # Iterate through pairs of primes p < q
    for q in four_digit_primes:
        for p in four_digit_primes:
            if p >= q:
                break

            # Oops! Skip the case given in the example!
            if p == 1487 and q == 4817:
                continue

            # Are p and q rearrangements?
            p_digits = list(to_digits(p))
            q_digits = list(to_digits(q))
            if sorted(p_digits) != sorted(q_digits):
                continue

            # Sequence is: p, q, q + (q-p) =: r
            r = 2 * q - p

            # Is r prime and a rearrangement of p/q?
            r_digits = list(to_digits(r))
            if is_prime(r) and sorted(p_digits) == sorted(r_digits):
                return from_digits(d for d in p_digits + q_digits + r_digits)

    raise AssertionError("no sequence found!")
