"""
Each character on a computer is assigned a unique code and the preferred standard is ASCII (American Standard Code for Information Interchange). For example, uppercase A = 65, asterisk (*) = 42, and lowercase k = 107.

A modern encryption method is to take a text file, convert the bytes to ASCII, then XOR each byte with a given value, taken from a secret key. The advantage with the XOR function is that using the same encryption key on the cipher text, restores the plain text; for example, 65 XOR 42 = 107, then 107 XOR 42 = 65.

For unbreakable encryption, the key is the same length as the plain text message, and the key is made up of random bytes. The user would keep the encrypted message and the encryption key in different locations, and without both "halves", it is impossible to decrypt the message.

Unfortunately, this method is impractical for most users, so the modified method is to use a password as a key. If the password is shorter than the message, which is likely, the key is repeated cyclically throughout the message. The balance for this method is using a sufficiently long password key for security, but short enough to be memorable.

Your task has been made easy, as the encryption key consists of three lower case characters. Using p059_cipher.txt (right click and 'Save Link/Target As...'), a file containing the encrypted ASCII codes, and the knowledge that the plain text must contain common English words, decrypt the message and find the sum of the ASCII values in the original text.
"""


from itertools import cycle, product
from typing import Iterator


def solve_problem() -> int:
    with open("resources/p059_cipher.txt") as f:
        text = f.read()
        ciphertext = bytes(int(s) for s in text.split(","))

    most_spaces = 0
    best_answer = None
    for key in generate_keys():
        plaintext = attempt_decryption(ciphertext, key)
        spaces = sum(1 for ch in plaintext if ch == " ")
        if spaces > most_spaces:
            most_spaces = spaces
            best_answer = plaintext

    # print(key) zzz? oh that's mean

    assert best_answer is not None
    return sum(ord(ch) for ch in best_answer)


def generate_keys() -> Iterator[str]:
    chars = [chr(n) for n in range(ord("a"), ord("z") + 1)]
    return iter("".join(tup) for tup in product(chars, repeat=3))


def attempt_decryption(ciphertext: bytes, key: str) -> str:
    return "".join(chr(byte ^ ord(ch)) for (byte, ch) in zip(ciphertext, cycle(key)))
