"""
A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit numbers is 9009 = 91 × 99.

Find the largest palindrome made from the product of two 3-digit numbers.
"""


def solve_problem() -> int:
    largest = 1
    for x in range(100, 1000):
        for y in range(100, 1000):
            z = x * y
            if z > largest and is_palindrome(z):
                largest = z
    return largest


def is_palindrome(x: int) -> bool:
    string = str(x)
    return string == "".join(reversed(string))
