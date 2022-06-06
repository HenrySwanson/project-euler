"""
In the United Kingdom the currency is made up of pound (£) and pence (p). There are eight coins in general circulation:

    1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).

It is possible to make £2 in the following way:

    1×£1 + 1×50p + 2×20p + 1×5p + 1×2p + 3×1p

How many different ways can £2 be made using any number of coins?
"""

from typing import List


def solve_problem() -> int:
    # This could be done with generating functions but I don't have the patience
    # right now for setting up that machinery.
    coins = [200, 100, 50, 20, 10, 5, 2, 1]
    return how_many_ways(coins, 200)


def how_many_ways(coins: List[int], total: int) -> int:
    assert coins
    coin = coins[0]

    if len(coins) == 1:
        return int(total % coin == 0)

    return sum(
        how_many_ways(coins[1:], total - n * coin) for n in range(total // coin + 1)
    )
