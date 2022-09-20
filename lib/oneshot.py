from typing import Dict, List, Sequence, Tuple
from lib.graph import node_costs_to_edge_costs


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


def p0081_convert_grid_to_graph(
    grid: Sequence[Sequence[int]], directions: List[Tuple[int, int]]
) -> Dict[Tuple[int, int], Dict[Tuple[int, int], int]]:
    # Problems 81-83 are all variants on the same theme, let's put them in the
    # same function

    height: int = len(grid)
    width: int = len(grid[0])
    assert all(len(row) == width for row in grid)

    # Convert to graph and apply Dijkstra
    def good_node(tup: Tuple[int, int]) -> bool:
        i, j = tup
        return 0 <= i < height and 0 <= j < width

    def neighbors(i: int, j: int) -> List[Tuple[int, int]]:
        possible = [(i + di, j + dj) for di, dj in directions]
        return [t for t in possible if good_node(t)]

    node_costs = {
        (i, j): cost for i, row in enumerate(grid) for j, cost in enumerate(row)
    }
    edges = {(i, j): neighbors(i, j) for i in range(height) for j in range(width)}
    return node_costs_to_edge_costs(node_costs, edges)
