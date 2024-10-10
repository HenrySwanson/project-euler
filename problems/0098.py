"""
By replacing each of the letters in the word CARE with 1, 2, 9, and 6
respectively, we form a square number: 1296 = 36^2. What is remarkable is that,
by using the same digital substitutions, the anagram, RACE, also forms a square
number: 9216 = 96^2. We shall call CARE (and RACE) a square anagram word pair
and specify further that leading zeroes are not permitted, neither may a
different letter have the same digital value as another letter.

Using words.txt (right click and 'Save Link/Target As...'), a 16K text file
containing nearly two-thousand common English words, find all the square anagram
word pairs (a palindromic word is NOT considered to be an anagram of itself).

What is the largest square number formed by any member of such a pair?

NOTE: All anagrams formed must be contained in the given text file.
"""

from collections import defaultdict
import itertools
import json
from math import isqrt
from typing import Dict, Iterable, List, Tuple, TypeVar

from lib.misc import from_digits, to_digits

T = TypeVar("T", str, int)


def solve_problem() -> int:
    # Load words
    with open("resources/0098_words.txt") as f:
        # hack to read the quoted words
        words = json.loads("[" + f.read() + "]")

    # Detect anagrams
    word_anagrams = make_anagram_map(words)
    for k, v in word_anagrams.items():
        # print(k, v)
        pass

    max_len = max(len(w) for w in word_anagrams)
    assert max_len == 9

    # Generate anagrammable squares
    square_anagrams = make_anagram_map(to_digits(x * x) for x in range(isqrt(10**9)))

    # Now we mash them together
    best = 0
    for letters, words in word_anagrams.items():
        for digits, squares in square_anagrams.items():
            if len(digits) != len(letters):
                continue

            # Now we can try to match up the squares with the words
            for w1, w2 in itertools.permutations(words, 2):
                for s1, s2 in itertools.permutations(squares, 2):
                    if test(w1, w2, s1, s2):
                        best = max(best, from_digits(s1), from_digits(s2))

    return best


def make_anagram_map(seqs: Iterable[Iterable[T]]) -> Dict[Tuple[T, ...], List[List[T]]]:
    map = defaultdict(list)
    for seq in seqs:
        sorted_seq = tuple(sorted(seq))
        map[sorted_seq].append(seq)
    return {k: v for k, v in map.items() if len(v) > 1}


def test(w1: List[str], w2: List[str], s1: List[int], s2: List[int]) -> bool:
    mapping = {}
    assert len(w1) == len(s1)
    for ch, d in zip(w1, s1):
        if ch in mapping:
            if mapping[ch] != d:
                return False
        else:
            mapping[ch] = d

    assert len(w2) == len(s2)
    for ch, d in zip(w2, s2):
        if ch in mapping:
            if mapping[ch] != d:
                return False
        else:
            mapping[ch] = d

    # No duplicate digits!
    return len(set(mapping.values())) == len(mapping)
