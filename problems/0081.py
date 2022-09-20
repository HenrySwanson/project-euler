"""
In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by only moving to the
right and down, is indicated in bold red and is equal to 2427.

(131)  673   234   103    18
(201)  (96) (342)  965   150
 630   803  (746) (422)  111
 537   699   497  (121)  956
 805   732   524   (37) (331)

Find the minimal path sum from the top left to the bottom right by only moving right and down in matrix.txt
(right click and "Save Link/Target As..."), a 31K text file containing an 80 by 80 matrix.
"""


from lib.graph import dijkstra
from lib.misc import parse_numeric_grid
from lib.oneshot import p0081_convert_grid_to_graph


def solve_problem() -> int:
    with open("resources/p081_matrix.txt") as f:
        contents = f.read()

    grid = parse_numeric_grid(contents, None, None, sep=",")
    assert len(grid) == 80
    assert all(len(row) == 80 for row in grid)

    # Convert to graph and apply Dijkstra
    dirs = [(1, 0), (0, 1)]
    edge_costs = p0081_convert_grid_to_graph(grid, dirs)

    # Lastly, add the initial edge into the graph (so that we count the first point)
    fake_start = (-1, -1)
    edge_costs[fake_start] = {(0, 0): grid[0][0]}

    return dijkstra(fake_start, (79, 79), edge_costs)
