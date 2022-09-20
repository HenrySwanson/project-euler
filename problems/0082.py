"""
NOTE: This problem is a more challenging version of Problem 81.

The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and finishing in
any cell in the right column, and only moving up, down, and right, is indicated in red and bold; the sum is
equal to 994.

 131   673  (234) (103)  (18)
(201)  (96) (342)  965   150
 630   803   746   422   111
 537   699   497   121   956
 805   732   524    37   331

Find the minimal path sum from the left column to the right column in matrix.txt (right click and 
"Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.
"""


from lib.graph import dijkstra
from lib.misc import parse_numeric_grid
from lib.oneshot import p0081_convert_grid_to_graph


def solve_problem() -> int:
    with open("resources/p082_matrix.txt") as f:
        contents = f.read()

    grid = parse_numeric_grid(contents, None, None, sep=",")
    assert len(grid) == 80
    assert all(len(row) == 80 for row in grid)

    # Convert to graph and apply Dijkstra
    dirs = [(1, 0), (0, 1), (-1, 0)]
    edge_costs = p0081_convert_grid_to_graph(grid, dirs)

    # Lastly, since we can start anywhere on the edges of the graph,
    # add in additional edges that come from a single start vertex,
    # and edges that lead to a single end vertex.
    fake_start = (-1, -1)
    fake_end = (-2, -2)
    edge_costs[fake_start] = {(i, 0): grid[i][0] for i in range(80)}
    for i in range(80):
        edge_costs[(i, 79)][fake_end] = 0

    return dijkstra(fake_start, fake_end, edge_costs)
