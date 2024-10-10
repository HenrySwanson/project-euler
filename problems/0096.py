"""
Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

<img src=project/images/p096_1.png,alt=p096_1.png></img>
<img src=project/images/p096_2.png,alt=p096_2.png></img>

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.
"""

from typing import Iterator, List, Tuple

from lib.misc import from_digits


Sudoku = List[List[int]]


def solve_problem() -> int:
    sudokus = load_sudokus()

    for s in sudokus:
        solve(s)

    return sum(from_digits(s[0][0:3]) for s in sudokus)


def load_sudokus() -> List[Sudoku]:
    with open("resources/p096_sudoku.txt") as f:
        lines = f.read().splitlines()

    grids = []
    for i in range(0, len(lines), 10):
        n = i // 10 + 1
        assert lines[i] == f"Grid {n:02}"
        grid_lines = lines[i + 1 : i + 10]
        grid = [[int(x) for x in row] for row in grid_lines]
        grids.append(grid)

    return grids


def solve(s: Sudoku) -> None:
    # Okay, first approach, see how long it takes, just do search
    # with backtracking.
    # If that's too slow, try constraint solving.
    success = solve_helper(s, 0, 0)
    assert success


def solve_helper(s: Sudoku, i: int, j: int) -> bool:
    if i >= 9:
        # we're at the end, it's solved!
        return True

    # what's the next cell?
    if j == 8:
        next_i, next_j = i + 1, 0
    else:
        next_i, next_j = i, j + 1

    # if this cell is decided, move to the next one
    if s[i][j] != 0:
        return solve_helper(s, next_i, next_j)

    # otherwise see what its possible values are
    forbidden = set(s[x][y] for x, y in get_buddies(i, j))
    allowed = set(range(1, 10)) - forbidden

    for d in allowed:
        s[i][j] = d
        if solve_helper(s, next_i, next_j):
            return True

    # no luck, reset to 0 and try again
    s[i][j] = 0
    return False


def get_buddies(i: int, j: int) -> Iterator[Tuple[int, int]]:
    # rows and columns
    for k in range(9):
        if k != i:
            yield (k, j)
        if k != j:
            yield (i, k)

    # what cell is it in? round to the upper left corner
    a = i // 3 * 3
    b = j // 3 * 3
    for m in range(a, a + 3):
        for n in range(b, b + 3):
            if (m, n) != (i, j):
                yield (m, n)
