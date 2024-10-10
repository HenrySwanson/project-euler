"""
Comparing two numbers written in index form like 2^11 and 3^7 is not difficult,
as any calculator would confirm that 2^11 = 2048 < 3^7 = 2187.

However, confirming that 632382^518061 > 519432^525806 would be much more
difficult, as both numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file
containing one thousand lines with a base/exponent pair on each line, determine
which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given
above.
"""

from math import log


def solve_problem() -> int:
    with open("resources/0099_base_exp.txt") as f:
        lines = f.readlines()

    data = [tuple(int(x) for x in line.split(",")) for line in lines]

    best = max(enumerate(data), key=lambda tup: tup[1][1] * log(tup[1][0]))

    return best[0] + 1
