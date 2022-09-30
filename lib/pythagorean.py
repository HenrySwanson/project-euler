# Iterate all primitive Pythagorean triples with one leg less than limit.
# These triples are ordered, so with limit = 10, this will return (3, 4, 5)
# and (4, 3, 5), but only (8, 15, 17), not (15, 8, 17).
from math import ceil, gcd, sqrt
from typing import Iterator, Tuple


def parameterize(m: int, n: int) -> Tuple[int, int, int]:
    a = (m * m - n * n) // 2
    b = m * n
    c = (m * m + n * n) // 2
    return (a, b, c)


def iter_primitive_pythagorean_by_perimeter(
    limit: int,
) -> Iterator[Tuple[int, int, int]]:
    # The perimeter is (m^2 - n^2) / 2 + mn + (m^2 + n^2)/2 = m^2 + mn,
    # and since n > 0, p > m^2.
    for m in range(1, ceil(sqrt(limit)), 2):
        for n in range(1, m, 2):
            term = m * (m + n)
            if term > limit:
                break

            if gcd(m, n) != 1:
                continue

            yield parameterize(m, n)


def iter_primitive_pythagorean_by_leg(limit: int) -> Iterator[Tuple[int, int, int]]:
    for m in range(1, limit, 2):
        for n in reversed(range(1, m, 2)):
            if gcd(m, n) != 1:
                continue

            (a, b, c) = parameterize(a, b)

            if a < limit:
                yield (a, b, c)
            else:
                break

        for n in range(1, m, 2):
            if gcd(m, n) != 1:
                continue

            (a, b, c) = parameterize(a, b)

            if b < limit:
                yield (b, a, c)
            else:
                break
