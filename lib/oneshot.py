from typing import Sequence


def p0018(triangle: Sequence[Sequence[int]]) -> int:
    # Let's do this via dynamic programming (so that Problem 67 will be free)

    # Note: len(triangle[i]) = i + 1
    scores = [[0 for _ in row] for row in triangle]

    scores[0][0] = triangle[0][0]
    for i in range(1, len(triangle)):
        for j in range(i + 1):
            candidates = []
            if j != i:
                candidates.append(scores[i - 1][j])
            if j != 0:
                candidates.append(scores[i - 1][j - 1])

            scores[i][j] = triangle[i][j] + max(candidates)

    return max(scores[-1])
