"""
We shall say that an n-digit number is pandigital if it makes use of all the digits 1 to n exactly once; for example, the 5-digit number, 15234, is 1 through 5 pandigital.

The product 7254 is unusual, as the identity, 39 × 186 = 7254, containing multiplicand, multiplier, and product is 1 through 9 pandigital.

Find the sum of all products whose multiplicand/multiplier/product identity can be written as a 1 through 9 pandigital.

HINT: Some products can be obtained in more than one way so be sure to only include it once in your sum.
"""

from lib.misc import digits


def solve_problem() -> int:
    # Two 3-digit numbers multiplied is never going to be a 3-digit number.
    # Similarly, 3-digits x 1-digit is never going to be 5 digits.
    # So if the first number is 3-digits, it must be 3-digits x 2-digits = 4-digits.
    # The only other possibility is 4-digits x 1-digit is 4-digits.
    products = set(
        x * y
        for x in range(100, 1000)
        for y in range(10, 100)
        if is_pandigital_product(x, y)
    ) | set(
        x * y
        for x in range(1000, 10000)
        for y in range(1, 10)
        if is_pandigital_product(x, y)
    )
    return sum(products)


def is_pandigital_product(x: int, y: int) -> bool:
    product = x * y
    all_digits = list(digits(x)) + list(digits(y)) + list(digits(product))
    return sorted(all_digits) == list(range(1, 10))
