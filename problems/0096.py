"""
Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

<img src=project/images/p096_1.png,alt=p096_1.png></img>
<img src=project/images/p096_2.png,alt=p096_2.png></img>

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.

The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).

By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.
"""

from typing import Iterator, List, Optional, Set, Tuple

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
    # Alternate constraint solving with guessing
    empties = {(i, j) for i in range(9) for j in range(9) if s[i][j] == 0}

    success = constraint_solve(s, empties)
    assert success


def constraint_solve(s: Sudoku, empties: Set[Tuple[int, int]]) -> bool:
    # Try to solve any empty squares
    original_empties = empties
    empties = set(empties)
    filled = []
    while True:
        modified_grid = False
        for i, j in empties:
            assert s[i][j] == 0

            forbidden = set(s[x][y] for x, y in get_buddies(i, j))
            allowed = set(range(1, 10)) - forbidden

            if len(allowed) == 0:
                # ran into a dead-end, clear the empties and back out
                for m, n in original_empties:
                    s[m][n] = 0
                return False

            if len(allowed) == 1:
                # great, we know we can fill this in
                s[i][j] = allowed.pop()
                filled.append((i, j))
                modified_grid = True

        # If we didn't change anything, time to break
        if not modified_grid:
            break

        # Otherwise, adjust empties list and try again
        empties.difference_update(filled)

    # Try the the guess step
    if try_to_guess(s, empties):
        return True

    # If it didn't work, reset the empties
    for m, n in original_empties:
        s[m][n] = 0
    return False


def try_to_guess(s: Sudoku, empties: Set[Tuple[int, int]]) -> bool:
    # Did we clear everything? If so, we won!
    if not empties:
        return True

    # Otherwise, let's guess something
    i, j = empties.pop()
    # see what its possible values are
    forbidden = set(s[x][y] for x, y in get_buddies(i, j))
    allowed = set(range(1, 10)) - forbidden

    for d in allowed:
        s[i][j] = d
        if constraint_solve(s, empties):
            return True

    # no luck, reset that cell and back out
    s[i][j] = 0
    empties.add((i, j))
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
