"""
All square roots are periodic when written as continued fractions and can be written in the form:

                              1
    sqrt(N) = a_0 + ----------------------
                               1
                    a_1 + ----------------
                                    1
                          a_2 + ---------
                                a_3 + ...

For example, let us consider sqrt(23):

    sqrt(23) = 4 + sqrt(23) - 4
             = 4 + 1 / 1 / (sqrt(23) - 4)
                             1
             = 1 + ----------------------
                   1 + (sqrt(23) - 3) / 7

If we continue we would get the following expansion:

                             1
    sqrt(23) = 4 + ----------------------
                              1
                   1 + ----------------
                                1
                       3 + -----------
                                  1
                           1 + -------
                               8 + ...

The process can be summarised as follows:

a_0 = 4    1 / (sqrt(23) - 4)  =  (sqrt(23) + 4) / 7   = 1 + (sqrt(23) - 3) / 7
a_1 = 1    7 / (sqrt(23) - 3)  = 7(sqrt(23) + 3) / 14  = 3 + (sqrt(23) - 3) / 2
a_2 = 3    2 / (sqrt(23) - 3)  = 2(sqrt(23) + 3) / 14  = 1 + (sqrt(23) - 4) / 7
a_3 = 1    7 / (sqrt(23) - 4)  = 7(sqrt(23) + 4) / 7   = 8 + (sqrt(23) - 4)
a_4 = 8    1 / (sqrt(23) - 4)  =  (sqrt(23) + 4) / 7   = 1 + (sqrt(23) - 3) / 7
a_5 = 1    7 / (sqrt(23) - 3)  = 7(sqrt(23) + 3) / 14  = 3 + (sqrt(23) - 3) / 2
a_6 = 3    2 / (sqrt(23) - 3)  = 2(sqrt(23) + 3) / 14  = 1 + (sqrt(23) - 4) / 7
a_7 = 1    7 / (sqrt(23) - 4)  = 7(sqrt(23) + 4) / 7   = 8 + (sqrt(23) - 4)

It can be seen that the sequence is repeating. For conciseness, we use the notation sqrt(23)=[4;(1,3,1,8)],
to indicate that the block (1,3,1,8) repeats indefinitely.

The first ten continued fraction representations of (irrational) square roots are:

    sqrt(2)  = [1;(2)]            period = 1
    sqrt(3)  = [1;(1,2)]          period = 2
    sqrt(3)  = [1;(1,2)]          period = 2
    sqrt(5)  = [2;(4)]            period = 1
    sqrt(6)  = [2;(2,4)]          period = 2
    sqrt(7)  = [2;(1,1,1,4)]      period = 4
    sqrt(8)  = [2;(1,4)]          period = 2
    sqrt(10) = [3;(6)]            period = 1
    sqrt(11) = [3;(3,6)]          period = 2
    sqrt(12) = [3;(2,6)]          period = 2
    sqrt(13) = [3;(1,1,1,1,6)]    period = 5 

Exactly four continued fractions, for N <= 13, have an odd period.

How many continued fractions for N <= 10000 have an odd period?
"""


from lib.cfrac import QuadraticCFrac


def solve_problem() -> int:
    total = 0
    for n in range(1, 10001):
        period = QuadraticCFrac.sqrt(n).period()
        if period is not None and period % 2 == 1:
            total += 1

    return total
