"""
If the numbers 1 to 5 are written out in words: one, two, three, four, five, then there are 3 + 3 + 5 + 4 + 4 = 19 letters used in total.

If all the numbers from 1 to 1000 (one thousand) inclusive were written out in words, how many letters would be used?

NOTE: Do not count spaces or hyphens. For example, 342 (three hundred and forty-two) contains 23 letters and 115 (one hundred and fifteen) contains 20 letters. The use of "and" when writing out numbers is in compliance with British usage.
"""

from typing import List

DIGIT_NAMES: List[str] = "zero one two three four five six seven eight nine".split()
TEENS_NAMES: List[
    str
] = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS_NAMES: List[
    str
] = "X X twenty thirty forty fifty sixty seventy eighty ninety".split()


def solve_problem() -> int:
    total = 0
    for n in range(1, 1001):
        total += len([x for x in spell_number(n) if x.isalpha()])

    return total


def spell_number(n: int) -> str:

    assert n <= 9999, "Can't handle numbers above 4 digits yet"

    thousands = n // 1000
    n %= 1000

    hundreds = n // 100
    n %= 100

    tens = n // 10
    n %= 10

    parts = []

    if thousands != 0:
        parts.append(f"{DIGIT_NAMES[thousands]} thousand")
    if hundreds != 0:
        parts.append(f"{DIGIT_NAMES[hundreds]} hundred")

    # Last two digits require care
    if tens == 0:
        if n != 0:
            parts.append(DIGIT_NAMES[n])
    elif tens == 1:
        parts.append(TEENS_NAMES[n])
    else:
        if n != 0:
            parts.append(f"{TENS_NAMES[tens]}-{DIGIT_NAMES[n]}")
        else:
            parts.append(f"{TENS_NAMES[tens]}")

    return " and ".join(parts)
