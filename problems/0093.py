"""
By using each of the digits from the set, {1, 2, 3, 4}, exactly once, and making use of the four arithmetic operations (+, −, *, /) and brackets/parentheses, it is possible to form different positive integer targets.

For example,

8 = (4 * (1 + 3)) / 2
14 = 4 * (3 + 1 / 2)
19 = 4 * (2 + 3) − 1
36 = 3 * 4 * (2 + 1)

Note that concatenations of the digits, like 12 + 34, are not allowed.

Using the set, {1, 2, 3, 4}, it is possible to obtain thirty-one different target numbers of which 36 is the maximum, and each of the numbers 1 to 28 can be obtained before encountering the first non-expressible number.

Find the set of four distinct digits, a < b < c < d, for which the longest set of consecutive positive integers, 1 to n, can be obtained, giving your answer as a string: abcd.
"""

from __future__ import annotations

import dataclasses
import itertools
from typing import List, Optional, Tuple

from lib.misc import from_digits


@dataclasses.dataclass(frozen=True)
class Expr:
    lhs: Expr | str
    op: str
    rhs: Expr | str

    def __str__(self) -> str:
        out: str
        if isinstance(self.lhs, str):
            out = self.lhs
        else:
            out = f"({ self.lhs})"

        out += f" {self.op} "

        if isinstance(self.rhs, str):
            out += self.rhs
        else:
            out += f"({ self.rhs})"

        return out


def solve_problem() -> int:
    # First we construct all the different possible expression trees.

    # Start with all possible triples of operations
    ops_combinations = list(itertools.product("+-*/", repeat=3))

    # There's only 5 possible patterns of parentheses:
    # - ((a o b) o c) o d
    # - (a o b) o (c o d)
    # - a o (b o (c o d))
    # - (a o (b o c)) o d
    # - a o ((b o c) o d)
    def make_exprs(ops: Tuple[str, str, str]) -> List[Expr]:
        x, y, z = ops
        return [
            Expr(
                lhs=Expr(lhs=Expr(lhs="a", op=x, rhs="b"), op=y, rhs="c"), op=z, rhs="d"
            ),
            Expr(
                lhs=Expr(lhs="a", op=x, rhs="b"), op=y, rhs=Expr(lhs="c", op=z, rhs="d")
            ),
            Expr(
                lhs="a", op=x, rhs=Expr(lhs="b", op=y, rhs=Expr(lhs="c", op=z, rhs="d"))
            ),
            Expr(
                lhs=Expr(lhs="a", op=x, rhs=Expr(lhs="b", op=y, rhs="c")), op=z, rhs="d"
            ),
            Expr(
                lhs="a", op=x, rhs=Expr(lhs=Expr(lhs="b", op=y, rhs="c"), op=z, rhs="d")
            ),
        ]

    exprs = [expr for ops in ops_combinations for expr in make_exprs(ops)]

    best_quartet = None
    best_score = 0

    for digits in itertools.combinations(range(1, 10), 4):
        answers = {
            evaluate(expr, quartet)
            for quartet in itertools.permutations(digits)
            for expr in exprs
        }

        for i in itertools.count(1):
            if i in answers:
                continue

            score = i - 1
            if score > best_score:
                best_quartet = digits
                best_score = score
            break

    return from_digits(best_quartet)


def evaluate(expr: Expr, quartet: Tuple[int, int, int, int]) -> Optional[int]:
    value = evaluate_helper(expr, quartet)
    if value is not None and int(value) == value:
        return int(value)
    return None


def evaluate_helper(
    expr: str | Expr, quartet: Tuple[int, int, int, int]
) -> Optional[float]:
    if isinstance(expr, str):
        idx = ord(expr) - ord("a")
        assert 0 <= idx < 4, expr
        return quartet[idx]

    # Otherwise, it's an Expr, evaluate the operation and the operands
    lhs = evaluate_helper(expr.lhs, quartet)
    rhs = evaluate_helper(expr.rhs, quartet)
    if lhs is None or rhs is None:
        return None
    if expr.op == "+":
        return lhs + rhs
    if expr.op == "-":
        return lhs - rhs
    if expr.op == "*":
        return lhs * rhs
    if expr.op == "/":
        return lhs / rhs if rhs != 0 else None
    raise AssertionError(f"Unrecognized operator {expr.op}")
