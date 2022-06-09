"""
The decimal number, 585 = 1001001001_2 (binary), is palindromic in both bases.

Find the sum of all numbers, less than one million, which are palindromic in base 10 and base 2.

(Please note that the palindromic number, in either base, may not include leading zeros.)
"""


def solve_problem() -> int:
    # Skip even numbers because they cannot be palindromic in base 2
    return sum(
        n
        for n in range(1, 1_000_000, 2)
        if is_palindromic_2(n) and is_palindromic_10(n)
    )


def is_palindromic_10(n: int) -> bool:
    s = str(n)
    return s == "".join(reversed(s))


def is_palindromic_2(n: int) -> bool:
    s = f"{n:b}"
    return s == "".join(reversed(s))
