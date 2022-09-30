"""
By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles:

6x     4x     2x
X--    XX-    XXX
---    ---    ---

3x     2x     1x
X--    XX-    XXX
X--    XX-    XXX

Although there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with the nearest solution.
"""

from math import isqrt


N = 2_000_000


def solve_problem() -> int:
    # This one's not too bad. An n x m rectangle contains (n+1) choose 2 * (m+1) choose 2
    # subrectangles (the bounds being "pick two fenceposts")
    # So we want the closest number to 2M of the form:
    #   (n+1)n/2 * (m+1)m/2
    # Note that: m^2 < m(m+1) < (m+1)^2, so if m(m+1) = x, m < sqrt(x) < m + 1
    best = None
    best_margin = 0
    for n in range(1, N):
        x = n * (n + 1) // 2

        if x > N / 2:
            break

        m_guess = isqrt(2 * N // x)

        for m in [m_guess, m_guess + 1]:
            product = x * m * (m + 1) // 2
            margin = abs(product - N)
            if best is None or margin < best_margin:
                best = (n, m)
                best_margin = margin

    assert best is not None
    return best[0] * best[1]
