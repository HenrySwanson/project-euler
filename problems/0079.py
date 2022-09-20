"""
A common security method used for online banking is to ask the user for three random characters
from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th
characters; the expected reply would be: 317.

The text file, keylog.txt, contains fifty successful login attempts.

Given that the three characters are always asked for in order, analyse the file so as to determine
the shortest possible secret passcode of unknown length.
"""


from collections import defaultdict
import itertools
from typing import Tuple

from lib.misc import from_digits, parse_numeric_list, to_digits


def solve_problem() -> int:
    # Basically, we're given (non-contiguous) substrings of the passcode, and we have
    # to stitch together the full thing.

    # Interesting, there's a solution with each digit exactly once! (Discovered by
    # inspection).
    # Knowing this, let's do a topological sort.

    with open("resources/p079_keylog.txt") as f:
        fragments = [
            tuple(to_digits(x)) for x in parse_numeric_list(f.read(), None, None)
        ]

    # Get edge data
    sources = defaultdict(set)  # all digits in sources[a] precede a
    for (a, b, c) in fragments:
        sources[c] |= {a, b}
        sources[b] |= {a}
        sources[a] |= set()

    # Now pull out digits one at a time
    solution = []
    while sources:
        leaders = [d for d, preds in sources.items() if not preds]
        assert len(leaders) == 1, f"Multiple possible leaders: {leaders}"
        leader = leaders[0]

        solution.append(leader)

        # Remove leader from sources
        del sources[leader]
        for srcs in sources.values():
            srcs.remove(leader)

    return from_digits(solution)
