from typing import Callable, Dict, List, Set
import itertools


def triangle(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 3
    return n * (n + 1) // 2


def square(n: int) -> int:
    return n * n


def pentagonal(n: int) -> int:
    # Convention: 0 -> 0, 1 -> 1, 2 -> 5
    return n * (3 * n - 1) // 2


def hexagonal(n: int) -> int:
    return n * (2 * n - 1)


def heptagonal(n: int) -> int:
    return n * (5 * n - 3) // 2


def octagonal(n: int) -> int:
    return n * (3 * n - 2)


def partition(n: int, cache: Dict[int, int]) -> int:
    # We use the recurrence relation to compute this
    if n < 0:
        return 0
    if n == 0:
        return 1

    if n in cache:
        return cache[n]

    total = 0
    for i in itertools.count(1):
        sign = 1 if i & 1 else -1

        p_k = pentagonal(i)
        total += sign * partition(n - p_k, cache)

        p_k = pentagonal(-i)
        total += sign * partition(n - p_k, cache)

        if p_k >= n:
            break

    cache[n] = total
    return total


# TODO: pull this and increasing_seq_cache into a class of some kind?
def increasing_seq_cutoff(f: Callable[[int], int], start: int, end: int) -> List[int]:
    assert start <= end
    values = []
    for n in itertools.count(0):
        value = f(n)
        if value < start:
            continue
        if value >= end:
            break
        values.append(value)

    return values


# TODO: don't like name :(
def increasing_seq_cache(f: Callable[[int], int]) -> Callable[[int], bool]:
    max_k: int = 0
    max_fk: int = f(0)
    cache: Set[int] = {max_fk}

    def inner(n: int) -> bool:
        nonlocal max_k, max_fk, cache
        while n > max_fk:
            max_k += 1
            max_fk = f(max_k)
            cache.add(max_fk)
        return n in cache

    return inner
