from __future__ import annotations
from fractions import Fraction
import itertools
import math
from typing import Iterable, Optional, Tuple


def nth_convergent(coeffs: Iterable[int], depth: int) -> Fraction:
    # Get the right number of coefficients
    coeffs = list(itertools.islice(coeffs, 0, depth))

    value = Fraction(coeffs[-1])
    for c in reversed(coeffs[:-1]):
        value = c + 1 / value

    return value


class QuadraticCFrac:
    head: Tuple[int, ...]
    tail: Optional[Tuple[int, ...]]

    def __init__(self, head: Iterable[int], tail: Optional[Iterable[int]]) -> None:
        self.head = tuple(head)
        if tail is None:
            self.tail = None
        else:
            self.tail = tuple(tail)

    @classmethod
    def sqrt(cls, n: int) -> QuadraticCFrac:
        # We want to track a number of the form (a + b * sqrt(n) / d)
        # and repeatedly find its continued fraction.
        sqrt_n = math.sqrt(n)

        a, b, d = 0, 1, 1
        history = []

        coeffs = []

        # Quadratics should repeat eventually, so this terminates
        while (a, b, d) not in history:
            history.append((a, b, d))

            # Get the integer part
            # (a+bX)/d = _ + (a'+bX)/d
            int_part = int((a + b * sqrt_n) / d)
            a -= int_part * d
            coeffs.append(int_part)

            # Now flip that fraction over, and rationalize the denominator
            # d/(a+bX) = d(-a+bX)/(b^2 n - a^2)

            # This could be zero in the denominator, if -a + b sqrt(n) is zero.
            # But then, sqrt(n) = a/b, which would mean n is a perfect square.
            (a, b, d) = (-d * a, d * b, b * b * n - a * a)

            if d == 0:
                assert a % b == 0
                return cls([a // b], None)

            # Check for common denominators
            g = math.gcd(a, b, d)
            (a, b, d) = (a // g, b // g, d // g)

        # Where did we see this number before? That's the first coefficent that
        # we repeat
        idx = history.index((a, b, d))
        return cls(coeffs[:idx], coeffs[idx:])

    def coeffs(self) -> Iterable[int]:
        if self.tail is None:
            return iter(self.head)
        else:
            return itertools.chain(self.head, itertools.cycle(self.tail))

    def period(self) -> Optional[int]:
        return len(self.tail) if self.tail else None
