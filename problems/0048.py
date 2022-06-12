"""
The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""

N = 10


def solve_problem() -> int:
    total = 0
    for n in range(1, 1001):
        total += pow(n, n, 10**N)
    return total % 10**N
