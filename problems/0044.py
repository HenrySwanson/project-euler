"""
Pentagonal numbers are generated by the formula, P_n=n(3n−1)/2. The first ten pentagonal numbers are:
1, 5, 12, 22, 35, 51, 70, 92, 117, 145, ...
It can be seen that P_4 + P_7 = 22 + 70 = 92 = P_8. However, their difference, 70 − 22 = 48, is not pentagonal.
Find the pair of pentagonal numbers, P_j and P_k, for which their sum and difference are pentagonal and D = |P_k − P_j| is minimised; what is the value of D?
"""


import itertools

from lib.misc import increasing_seq_cache, pentagonal


def solve_problem() -> int:
    is_pentagonal = increasing_seq_cache(pentagonal)

    # We want to iterate over pairs (j, k) where j < k.
    # I think iterating in this order guarantees we find the minimum? IDK though...
    # TODO: prove
    for k in itertools.count(1):
        p_k = pentagonal(k)
        for j in range(1, k):
            p_j = pentagonal(j)
            if is_pentagonal(p_k + p_j) and is_pentagonal(p_k - p_j):
                return p_k - p_j

    raise AssertionError()