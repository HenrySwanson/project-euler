"""
It is easily proved that no equilateral triangle exists with integral length sides and integral area. However, the almost equilateral triangle 5-5-6 has an area of 12 square units.

We shall define an almost equilateral triangle to be a triangle for which two sides are equal and the third differs by no more than one unit.

Find the sum of the perimeters of all almost equilateral triangles with integral side lengths and area and whose perimeters do not exceed one billion (1,000,000,000).
"""

ONE_BILLION = 1_000_000_000


def solve_problem() -> int:
    # The side lengths are, by definition, n, n, and n ± 1. If n is even, then the semi-perimeter
    # is a half integer, and so its area is not an integer (Heron's formula).
    # So n is odd, and the side lengths are: 2k, 2k±1, 2k±1.
    #
    # Now apply Heron's formula to get the area. Semiperimeter s is 3k±1, so:
    #     A^2 = s(s-a)(s-b)(s-c) = (3k±1)(k±1)kk
    # To get an integer area, we need (3k±1)(k±1) to be a perfect square.
    #
    # Let's rearrange (3k±1)(k±1) = y^2:
    #   (3k±1)(k±1) - y^2 = 0
    #   3k^2 ± 4k + 1 - y^2 = 0
    #   9k^2 ± 12k + 3 - 3y^2 = 0
    #   (3k±2)^2 - 3y^2 = 1
    #
    # Great, that's a Pell equation! For a solution (x, y), we have x = 3k±2,
    # so k = (x∓2)/3. Only one of the signs will work for any given x.
    #
    # The trivial solution (1, 0) gives k = 1 (taking the bottom branch), so the
    # sides are (2, 1, 1). Integer area to be sure, but not a triangle.
    #
    # Manually solving, the fundamental solution is (2, 1). This gives k = 0
    # (top branch), and sides (0, 1, 1). Also not a triangle.
    #
    # So we'll go take powers of the fundamental solution, alternating signs,
    # until the perimeter gets too big.
    perimeter_sum = 0
    x, y = 2, 1
    sign = 1
    while True:
        # (x + y√3)(2 + 1√3) = 2x + x√3 + 2y√3 + 3y
        x, y = 2 * x + 3 * y, x + 2 * y
        # flip the sign
        sign = -sign

        # Confirm it's still a solution
        assert x * x - 3 * y * y == 1, f"({x}, {y})"

        # We could compute k directly, but we can actually jump
        # straight to the perimeter.
        # Since the sides are (2k, 2k±1, 2k±1), the perimeter is 6k±2.
        # Plugging in k = (x∓2)/3, we get P = 2(x∓2)±2 = 2x∓2

        perimeter = 2 * (x - sign)
        if perimeter > ONE_BILLION:
            break

        perimeter_sum += perimeter

    return perimeter_sum
