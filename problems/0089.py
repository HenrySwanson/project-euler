"""
For a number written in Roman numerals to be considered valid there are basic rules which must be followed. Even though the rules allow some numbers to be expressed in more than one way there is always a "best" way of writing a particular number.

For example, it would appear that there are at least six ways of writing the number sixteen:

IIIIIIIIIIIIIIII
VIIIIIIIIIII
VVIIIIII
XIIIIII
VVVI
XVI

However, according to the rules only <span class=monospace>XIIIIII</span> and <span class=monospace>XVI</span> are valid, and the last example is considered to be the most efficient, as it uses the least number of numerals.

The 11K text file, roman.txt (right click and 'Save Link/Target As...'), contains one thousand numbers written in valid, but not necessarily minimal, Roman numerals; see About... Roman Numerals for the definitive rules for this problem.

Find the number of characters saved by writing each of these in their minimal form.

Note: You can assume that all the Roman numerals in the file contain no more than four consecutive identical units.
"""

from typing import List, Tuple

SIMPLEST_STRS: List[str] = "|I|II|III|IV|V|VI|VII|VIII|IX".split("|")


def solve_problem() -> int:
    with open("resources/p089_roman.txt") as f:
        numerals = f.readlines()

    return sum(get_character_excess(r) for r in numerals)


def get_character_excess(roman: str) -> int:
    # chomp through the Ms, since they'll always be Ms
    i: int = 0
    while i < len(roman) and roman[i] == "M":
        i += 1

    # helper fn to avoid repeating things a bunch
    def _parse_roman_numeral(ones: str, fives: str, tens: str) -> int:
        nonlocal i
        start = i
        total = 0
        while i < len(roman):
            ch = roman[i]
            if ch == ones:
                total += 1
            elif ch == fives:
                total += 5
            elif ch == tens:
                assert total == 1
                total = 10 - total
            else:
                break

            i += 1

        # take the length of our substring and subtract off the ideal length
        return (i - start) - len(SIMPLEST_STRS[total])

    # investigate the hundreds place: CDM
    excess_hundreds = _parse_roman_numeral("C", "D", "M")
    excess_tens = _parse_roman_numeral("X", "L", "C")
    excess_ones = _parse_roman_numeral("I", "V", "X")

    return excess_hundreds + excess_tens + excess_ones
