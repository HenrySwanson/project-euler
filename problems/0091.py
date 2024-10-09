"""
The points P (x_1, y_1) and Q (x_2, y_2) are plotted at integer co-ordinates and are joined to the origin, O(0,0), to form ΔOPQ.

There are exactly fourteen triangles containing a right angle that can be formed when each co-ordinate lies between 0 and 2 inclusive; that is,
0 ≤ x_1, y_1, x_2, y_2 ≤ 2.

Given that 0 ≤ x_1, y_1, x_2, y_2 ≤ 50, how many right triangles can be formed?
"""

from math import gcd


N = 50


def solve_problem() -> int:
    # How many triangles have a right angle at the origin? Just pick one point on
    # each axis.
    total = N * N

    # How about the other triangles? Let's call the vertex with the right angle P.
    # We can put P just about anywhere, so let's select it first.
    for a in range(N + 1):
        for b in range(N + 1):
            # P can't be at the origin
            if a == 0 and b == 0:
                continue

            # Okay, let's find triangles with right angle at P.
            # Draw a vector perpendicular to OP, and then march along it and see what
            # lattice points we hit. Remember to march in both directions.
            #
            # One such vector is (-b, a), which we reduce to lowest terms.
            g = gcd(a, b)
            u, v = -b // g, a // g

            for k in range(-N, N + 1):
                if k == 0:
                    continue
                q = (a + u * k, b + v * k)
                if 0 <= q[0] <= N and 0 <= q[1] <= N:
                    total += 1

    return total
