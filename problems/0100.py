"""
If a box contains twenty-one coloured discs, composed of fifteen blue discs and
six red discs, and two discs were taken at random, it can be seen that the
probability of taking two blue discs, P(BB) = (15/21)×(14/20) = 1/2.

The next such arrangement, for which there is exactly 50% chance of taking two
blue discs at random, is a box containing eighty-five blue discs and thirty-five
red discs.

By finding the first arrangement to contain over 10^12 = 1,000,000,000,000 discs
in total, determine the number of blue discs that the box would contain.
"""

LIMIT = 10**12


def solve_problem() -> int:
    # This is another Pell equation problem.
    #
    # We need to find integer b and t (blue and total) such that b/t*(b-1)/(t-1)
    # is exactly 1/2.
    #
    # Rearranging that, we get 2b(b-1) = t(t-1). Taking the solutions from the
    # example, we get (b,t) = (15,21); does 2*15*14 = 21*20? Yep.
    #
    # Completing the square for x(x-1) is (x-1/2)^2 - 1/4, so let's multiply
    # through by 4: 4x(x-1) = (2x-1)^2 - 1.
    # Applying that to our equation:
    #     2 [(2b-1)^2 - 1] = (2t-1)^2 - 1
    #     -1 = (2t-1)^2 - 2(2b-1)^2
    #
    # So, with x = 2t-1, y = 2b-1, we have:
    #     x^2 - 2y^2 = -1
    #
    # Okay so it's negative Pell's equation. Close enough.
    # The original solution has (x,y) = (41,29), and indeed, 41^2 - 2*29^2 is -1.
    #
    # The fundamental solution for this one is pretty easy to guess: (1,1).
    # It doesn't correspond to a realistic urn (b=1, t=1), but that's okay, we
    # don't need it to.
    #
    # Remember to take odd powers only (or else you get +1).

    x, y = 1, 1
    while True:
        # TODO: factor out pell multiplication into some helper function
        # (x+y√2)(1+√2) = (x + 2y) + (x + y)√2
        x, y = x + 2 * y, x + y
        x, y = x + 2 * y, x + y

        # Sanity check
        assert x * x - 2 * y * y == -1

        # Get total number of discs
        t = (x + 1) // 2

        if t > LIMIT:
            b = (y + 1) // 2
            return b
    ...
