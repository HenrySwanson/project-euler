from typing import Optional, Sequence, Tuple, TypeVar

T = TypeVar("T")


def parse_numeric_list(
    input: str, start_line: Optional[int], end_line: Optional[int]
) -> Tuple[int, ...]:
    return tuple(
        int(line) for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


def parse_numeric_grid(
    input: str, start_line: Optional[int], end_line: Optional[int], sep: str = " "
) -> Tuple[Tuple[int, ...], ...]:
    return tuple(
        tuple(int(x) for x in line.split(sep))
        for line in _ext_slice(input.splitlines(), start_line, end_line)
    )


# TODO: there's gotta be something in python that does this
def _ext_slice(s: Sequence[T], start: Optional[int], end: Optional[int]) -> Sequence[T]:
    if start is not None:
        if end is not None:
            return s[start:end]
        else:
            return s[start:]
    else:
        if end is not None:
            return s[:end]
        else:
            return s
