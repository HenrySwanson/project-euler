"""
You are given the following information, but you may prefer to do some research for yourself.

    1 Jan 1900 was a Monday.
    Thirty days has September,
    April, June and November.
    All the rest have thirty-one,
    Saving February alone,
    Which has twenty-eight, rain or shine.
    And on leap years, twenty-nine.
    A leap year occurs on any year evenly divisible by 4, but not on a century unless it is divisible by 400.

How many Sundays fell on the first of the month during the twentieth century (1 Jan 1901 to 31 Dec 2000)?
"""

MONTH_LENGTH = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def solve_problem() -> int:
    # Using datetime for this would be 100% cheating :)
    # Let's track what weekday the first of the month falls on.
    # Sunday = 0

    total = 0
    weekday = 1
    for y in range(1900, 2001):
        for m in range(1, 13):
            # Check for Sunday (only starting at 1901 though)
            if weekday == 0 and y >= 1901:
                total += 1

            # Increment the counter by a month
            weekday += MONTH_LENGTH[m]

            # Account for leap days!
            if m == 2 and is_leap_year(y):
                weekday += 1

            weekday %= 7

    return total


def is_leap_year(year: int) -> bool:
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0
