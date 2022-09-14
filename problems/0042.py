"""
The n^th term of the sequence of triangle numbers is given by, t_n = ½n(n+1); so the first ten triangle numbers are:
1, 3, 6, 10, 15, 21, 28, 36, 45, 55, ...
By converting each letter in a word to a number corresponding to its alphabetical position and adding these values we form a word value. For example, the word value for SKY is 19 + 11 + 25 = 55 = t_10. If the word value is a triangle number then we shall call the word a triangle word.
Using <a>words.txt</a> (right click and 'Save Link/Target As...'), a 16K text file containing nearly two-thousand common English words, how many are triangle words?
"""


import itertools
from lib.sequence import triangle


def solve_problem() -> int:
    with open("resources/p042_words.txt") as f:
        words = [w.strip('"') for w in f.read().split(",")]

    max_len = max(len(w) for w in words)
    triangles = list(
        itertools.takewhile(
            lambda t: t < 26 * max_len,
            iter(triangle(n) for n in itertools.count()),
        )
    )

    return sum(1 for w in words if score(w) in triangles)


def score(word: str) -> int:
    return sum(ord(ch) - ord("A") + 1 for ch in word.upper())
