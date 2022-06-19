"""
In the card game poker, a hand consists of five cards and are ranked, from lowest to highest, in the following way:

- High Card: Highest value card.
- One Pair: Two cards of the same value.
- Two Pairs: Two different pairs.
- Three of a Kind: Three cards of the same value.
- Straight: All cards are consecutive values.
- Flush: All cards of the same suit.
- Full House: Three of a kind and a pair.
- Four of a Kind: Four cards of the same value.
- Straight Flush: All cards are consecutive values of same suit.
- Royal Flush: Ten, Jack, Queen, King, Ace, in same suit.

The cards are valued in the order:
2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace.

If two players have the same ranked hands then the rank made up of the highest value wins; for example, a pair of eights beats a pair of fives (see example 1 below). But if two ranks tie, for example, both players have a pair of queens, then highest cards in each hand are compared (see example 4 below); if the highest cards tie then the next highest cards are compared, and so on.

Consider the following five hands dealt to two players:

Hand     Player 1               Player 2              Winner
1        5H 5C 6S 7S KD         2C 3S 8S 8D TD        Player 2
         Pair of Fives          Pair of Eights
2        5D 8C 9S JS AC         2C 5C 7D 8S QH        Player 1
         Highest card Ace       Highest Card Queen
3        2D 9C AS AH AC         3D 6D 7D TD QD        Player 2
         Three Aces             Flush with Diamonds
4        4D 6S 9H QH QC         3D 6D 7H QD QS        Player 1
         Pair of Queens         Pair of Queens
         Highest Card Nine      Highest Card Seven
5        2H 2D 4C 4D 4S         3C 3D 3S 9S 9D        Player 1
         Full House             Full House
         With Three Fours       With Three Threes

The file, poker.txt, contains one-thousand random hands dealt to two players. Each line of the file contains ten cards (separated by a single space): the first five are Player 1's cards and the last five are Player 2's cards. You can assume that all hands are valid (no invalid characters or repeated cards), each player's hand is in no specific order, and in each hand there is a clear winner.

How many hands does Player 1 win?
"""

from __future__ import annotations

import abc
from collections import Counter, defaultdict
import dataclasses
from enum import IntEnum, auto
import functools
from typing import ClassVar, Dict, List, Optional, TypeVar


def solve_problem() -> int:
    # This just seems tedious. Lots of case bashing.
    total_wins = 0
    with open("resources/p054_poker.txt") as f:
        for line in f.readlines():
            cards = [Card.from_string(s) for s in line.split()]
            assert len(cards) == 10
            lhs = analyze_hand(cards[:5])
            rhs = analyze_hand(cards[5:])

            assert lhs != rhs, f"Shouldn't have two equal hands: {cards}"
            total_wins += int(lhs.beats(rhs))

    return total_wins


@dataclasses.dataclass
class Card:
    rank: int
    suit: str

    TEN: ClassVar[int] = 10
    JACK: ClassVar[int] = 11
    QUEEN: ClassVar[int] = 12
    KING: ClassVar[int] = 13
    ACE: ClassVar[int] = 14

    RANK_DICT: ClassVar[Dict[str, int]] = {
        "T": TEN,
        "J": JACK,
        "Q": QUEEN,
        "K": KING,
        "A": ACE,
    }

    @classmethod
    def from_string(cls, s: str) -> Card:
        assert len(s) == 2
        r = s[0]
        rank = cls.RANK_DICT.get(r, None) or int(r)
        suit = s[1]
        return Card(rank=rank, suit=suit)


class HandKind(IntEnum):
    HighCard = auto()
    OnePair = auto()
    TwoPairs = auto()
    ThreeOfAKind = auto()
    Straight = auto()
    Flush = auto()
    FullHouse = auto()
    FourOfAKind = auto()
    StraightFlush = auto()
    RoyalFlush = auto()


@dataclasses.dataclass
class HandInfo:
    # What kind of hand it is
    kind: HandKind
    # Ranks used for tiebreaking
    # For example, a full house with three 2s and two jacks is [2, J]
    # A 5-9 straight is [9, 8, 7, 6, 5].
    # A pair of 2s with other cards X,Y,Z will be [2, X, Y, Z].
    relevant_ranks: List[int]

    def beats(self, other: HandInfo) -> bool:
        if self.kind > other.kind:
            return True
        elif self.kind < other.kind:
            return False
        else:
            return self.relevant_ranks > other.relevant_ranks


def analyze_hand(cards: List[Card]) -> HandInfo:
    sorted_ranks = sorted(c.rank for c in cards)
    reversed_ranks = list(reversed(sorted_ranks))

    is_flush = len(set(c.suit for c in cards)) == 1
    is_straight = sorted_ranks == list(range(sorted_ranks[0], sorted_ranks[-1] + 1))

    # We have to be a little careful identifying the hand kind, because there's overlap.
    # Not as much as you'd think though.
    #
    # There's overlap between OnePair, TwoPair, ThreeOfAKind, FullHouse, and FourOfAKind,
    # but none of those overlap with straights or flushes.
    #
    # Similarly, straights and flushes only overlap as straight (or royal) flushes.

    kind: HandKind
    relevant_ranks: List[int]
    if is_straight and is_flush:
        highest_card = sorted_ranks[-1]
        is_royal = highest_card == Card.ACE
        kind = HandKind.RoyalFlush if is_royal else HandKind.StraightFlush
        relevant_ranks = reversed_ranks
    elif is_flush:
        kind = HandKind.Flush
        relevant_ranks = reversed_ranks
    elif is_straight:
        kind = HandKind.Straight
        relevant_ranks = reversed_ranks
    else:
        # Okay, so it's one of the pair-based ones.
        # Build a list of card ranks, sorted by most-relevant to least
        # (e.g., for a two-pair hand, it's highest pair, lowest pair, singlet).
        counter = Counter(sorted_ranks)
        # Sort by frequency, then by value, both descending
        relevant_ranks = sorted(sorted_ranks, key=lambda rank: (-counter[rank], -rank))

        how_many_twos = list(counter.values()).count(2)
        if 4 in counter.values():
            kind = HandKind.FourOfAKind
        elif 3 in counter.values():
            kind = HandKind.FullHouse if how_many_twos == 1 else HandKind.ThreeOfAKind
        elif how_many_twos == 2:
            kind = HandKind.TwoPairs
        elif how_many_twos == 1:
            kind = HandKind.OnePair
        else:
            kind = HandKind.HighCard

    return HandInfo(kind=kind, relevant_ranks=relevant_ranks)
