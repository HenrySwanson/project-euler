"""
Using names.txt (right click and 'Save Link/Target As...'), a 46K text file containing over five-thousand first names, begin by sorting it into alphabetical order. Then working out the alphabetical value for each name, multiply this value by its alphabetical position in the list to obtain a name score.

For example, when the list is sorted into alphabetical order, COLIN, which is worth 3 + 15 + 12 + 9 + 14 = 53, is the 938th name in the list. So, COLIN would obtain a score of 938 × 53 = 49714.

What is the total of all the name scores in the file?
"""


def solve_problem() -> int:
    with open("resources/p022_names.txt", "r") as f:
        names = sorted(x.strip('"') for x in f.read().split(","))

    return sum((i + 1) * alphabetical_score(name) for (i, name) in enumerate(names))


def alphabetical_score(name: str) -> int:
    return sum(ord(ch) - ord("A") + 1 for ch in name.upper())
