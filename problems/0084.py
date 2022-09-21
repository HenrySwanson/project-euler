DESCRIPTION = """
In the game, Monopoly, the standard board is set up in the following way:
GO  A1  CC1 A2  T1  R1  B1  CH1 B2  B3  JAIL
H2                                      C1
T2                                      U1
H1                                      C2
CH3                                     C3
R4                                      R2
G3                                      D1
CC3                                     CC2
G2                                      D2
G1                                      D3
G2J F3  U2  F2  F1  R3  E3  E2  CH2 E1  FP

A player starts on the GO square and adds the scores on two 6-sided dice to determine
the number of squares they advance in a clockwise direction. Without any further rules
we would expect to visit each square with equal probability: 2.5%. However, landing on
G2J (Go To Jail), CC (community chest), and CH (chance) changes this distribution.

In addition to G2J, and one card from each of CC and CH, that orders the player to go
directly to jail, if a player rolls three consecutive doubles, they do not advance the
result of their 3rd roll. Instead they proceed directly to jail.

At the beginning of the game, the CC and CH cards are shuffled. When a player lands on
CC or CH they take a card from the top of the respective pile and, after following the
instructions, it is returned to the bottom of the pile. There are sixteen cards in each
pile, but for the purpose of this problem we are only concerned with cards that order a
movement; any instruction not concerned with movement will be ignored and the player
will remain on the CC/CH square.

- Community Chest (2/16 cards):
  1. Advance to GO
  2. Go to JAIL  
- Chance (10/16 cards):
  1. Advance to GO
  2. Go to JAIL
  3. Go to C1
  4. Go to E3
  5. Go to H2
  6. Go to R1
  7. Go to next R (railway company)
  8. Go to next R
  9. Go to next U (utility company)
  10. Go back 3 squares.  

The heart of this problem concerns the likelihood of visiting a particular square. That is,
the probability of finishing at that square after a roll. For this reason it should be clear
that, with the exception of G2J for which the probability of finishing on it is zero, the
CH squares will have the lowest probabilities, as 5/8 request a movement to another square,
and it is the final square that the player finishes at on each roll that we are interested
in. We shall make no distinction between "Just Visiting" and being sent to JAIL, and we shall
also ignore the rule about requiring a double to "get out of jail", assuming that they pay
to get out on their next turn.

By starting at GO and numbering the squares sequentially from 00 to 39 we can concatenate
these two-digit numbers to produce strings that correspond with sets of squares.

Statistically it can be shown that the three most popular squares, in order, are
  JAIL (6.24%) = Square 10
  E3 (3.18%) = Square 24
  GO (3.09%) = Square 00
  
So these three most popular squares can be listed with the six-digit modal string: 102400.

If, instead of using two 6-sided dice, two 4-sided dice are used, find the six-digit modal string.
"""

from collections import defaultdict
import itertools
from typing import Dict, List, Literal, Tuple, Union

from lib.misc import from_digits, num_digits


N = 4
TOLERANCE = 1e-7


def solve_problem() -> int:
    # Hoo boy this will be a long one.

    # First load the board
    cells = [row.split() for row in DESCRIPTION.splitlines()[2:13]]
    squares = cells[0]
    squares += [sq for (_, sq) in cells[1:-1]]
    squares += reversed(cells[-1])
    squares += [sq for (sq, _) in reversed(cells[1:-1])]
    num_squares = len(squares)

    # Some additional data structures for convenience
    name_lookup = {name: i for i, name in enumerate(squares)}
    jail_idx = name_lookup["JAIL"]

    # Now we figure out the "you don't land on this square, move here" probabilities
    jump_probabilities = get_jump_probabilities(squares)

    # Next, we need the probabilities from the dice
    dice_probabilities: Dict[Tuple[int, bool], float] = defaultdict(float)
    for d1, d2 in itertools.product(range(1, N + 1), repeat=2):
        is_double = d1 == d2
        dice_probabilities[(d1 + d2, is_double)] += 1 / N / N

    # Finally, we can compute the transition probabilities for the whole board.
    # But we need to include "number of doubles" in our state...
    states = [(dst, doubles) for dst in range(num_squares) for doubles in [0, 1, 2]]
    transition_probabilities = {src: {dst: 0.0 for dst in states} for src in states}
    for src in states:
        # Where can the dice take us?
        for ((dice_sum, rolled_double), dice_prob) in dice_probabilities.items():

            # They could take us right to jail!
            num_doubles = src[1] + 1 if rolled_double else 0
            if num_doubles == 3:
                transition_probabilities[src][(jail_idx, 0)] += dice_prob
                continue

            # Otherwise it's a normal roll
            dst_sq = (src[0] + dice_sum) % num_squares
            dst_name = squares[dst_sq]

            # When we land, what's the probability of jumping elsewhere?
            non_jump_prob = 1
            for (target, jump_prob) in jump_probabilities.get(dst_name, []):
                jump_target = (name_lookup[target], num_doubles)
                transition_probabilities[src][jump_target] += dice_prob * jump_prob
                non_jump_prob -= jump_prob

            # If we don't jump, record that too
            dst = (dst_sq, num_doubles)
            transition_probabilities[src][dst] += dice_prob * non_jump_prob

    # This should be a legit transition matrix, columns sum to 1
    for i in states:
        row_sum = sum(transition_probabilities[i][j] for j in states)
        assert 0.9999 < row_sum < 1.0001, row_sum

    # Now find a stationary distribution for it
    # Let's try this experimentally first, b/c I don't want to program matrices yet
    # TODO: come back to this...
    distribution = {s: float(s == (0, 0)) for s in states}
    while True:
        new_distribution = {
            dst: sum(
                iter(
                    transition_probabilities[src][dst] * distribution[src]
                    for src in states
                ),
                start=0.0,
            )
            for dst in states
        }

        if all(abs(distribution[s] - new_distribution[s]) < TOLERANCE for s in states):
            break

        distribution = new_distribution

    # Now, regroup the states without keeping track of doubles
    reduced_distribution = [0.0 for _ in range(num_squares)]
    for (i, _), prob in distribution.items():
        reduced_distribution[i] += prob

    freq_sorted = sorted(enumerate(reduced_distribution), key=lambda t: -t[1])
    top_three = freq_sorted[:3]

    # for i in range(num_squares):
    #     print("{:4}: {:.4}%".format(squares[i], 100 * reduced_distribution[i]))
    # print("SUM = ", sum(reduced_distribution))
    # print(top_three)

    return sum(100 ** (2 - i) * sq_num for i, (sq_num, _) in enumerate(top_three))


def get_jump_probabilities(squares: List[str]) -> Dict[str, List[Tuple[str, float]]]:
    jump_probabilities: Dict[str, List[Tuple[str, float]]] = {}

    for (self_idx, square) in enumerate(squares):
        # Go to jail!
        if square == "G2J":
            jump_probabilities[square] = [("JAIL", 1.0)]
        # Figure out community chest probabilities
        if square.startswith("CC"):
            jump_probabilities[square] = [
                ("GO", 1 / 16),
                ("JAIL", 1 / 16),
            ]

        # Figure out chance probabilities
        if square.startswith("CH"):
            next_rr = next(
                sq
                for i, sq in enumerate(itertools.cycle(squares))
                if i > self_idx and sq.startswith("R")
            )
            next_util = next(
                sq
                for i, sq in enumerate(itertools.cycle(squares))
                if i > self_idx and sq.startswith("U")
            )
            prev_3 = squares[self_idx - 3]

            jump_probabilities[square] = [
                ("GO", 1 / 16),
                ("JAIL", 1 / 16),
                ("C1", 1 / 16),
                ("E3", 1 / 16),
                ("H2", 1 / 16),
                ("R1", 1 / 16),
                (next_rr, 2 / 16),  # not typo!
                (next_util, 1 / 16),
                (prev_3, 1 / 16),
            ]

    return jump_probabilities
