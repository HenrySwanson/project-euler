from typing import Iterable, List, Optional, Tuple


def intervalize(numbers: Iterable[int]) -> List[Tuple[int, int]]:
    """
    Given an collection of integers, groups them into contiguous intervals.
    Intervals are reported with both endpoints inclusive, and single integers are
    reported as (a, a).
    """
    numbers = sorted(numbers)

    if not numbers:
        return []

    intervals = []

    start = numbers[0]  # start point of current interval
    for prev, n in zip(numbers, numbers[1:]):
        if start is None:
            start = prev

        if n == prev + 1:
            continue

        intervals.append((start, prev))
        start = n

    # Make sure to close the last interval.
    intervals.append((start, numbers[-1]))

    return intervals


def format_as_intervals(
    numbers: Iterable[int], infinite_tail: Optional[int] = None
) -> str:
    """
    Pretty-prints the collection of numbers by grouping them into intervals and printing
    the intervals.

    Able to handle certain infinite collections by specifying `infinite_tail=n` (all
    integers at least n are included in the set.)
    """
    intervals = intervalize(numbers)

    # If there's an infinite tail, and it overlaps or is adjacent to any of the intervals,
    # merge those intervals into the tail.
    if infinite_tail is not None:
        while len(intervals) > 0:
            (start, end) = intervals[-1]
            # `end+1` so that (5, 10) will merge with infinite_tail=11
            if infinite_tail <= end + 1:
                infinite_tail = min(start, infinite_tail)
                intervals.pop()

    # Stringify things
    output = [
        f"{start}-{end}" if start != end else f"{start}" for (start, end) in intervals
    ]

    if infinite_tail is not None:
        output.append(f"{infinite_tail}-inf")

    return ", ".join(output)


def parse_interval_string(s: str) -> Tuple[int, int]:
    try:
        x = int(s)
        return (x, x)
    except ValueError:
        pass

    # This ValueError through, we want to throw
    start, end = s.split("-")
    return (int(start), int(end))
