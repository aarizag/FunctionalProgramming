from typing import List
from pyrsistent import v, pvector


"""
Luhn Algorithm to determine if an account number is considered valid.

Source: https://en.wikipedia.org/wiki/Luhn_algorithm
"""
def luhn_wiki(purported):
    """
    >>> luhn_wiki(79927398713)
    True
    >>> luhn_wiki(79927398714)
    False
    """
    LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8, 1, 3, 5, 7, 9)  # sum_of_digits (index * 2)

    if not isinstance(purported, str):
        purported = str(purported)
    try:
        evens = sum(int(p) for p in purported[-1::-2])
        odds = sum(LUHN_ODD_LOOKUP[int(p)] for p in purported[-2::-2])
        return (evens + odds) % 10 == 0
    except ValueError:  # Raised if an int conversion fails
        return False


"""
Standard implementation of the Luhn Algorithm
"""
def luhn_standard(account_num: int, check_digit: int = 0) -> bool:
    # Seperate number into a list.
    # Convert the number to a string, then iterate through string converting back to int at each item
    def sep_digits(num: int) -> List[int]:
        # Doing math operations is slower at larger number of digits and negligibly faster at small numbers
        # return [] if num == 0 else sep_digits(num // 10) + [num % 10]
        return [int(x) for x in str(num)]

    # Double every other number in a list starting at the end of the list and sum the new total
    def double_and_sum() -> int:
        digit_list = sep_digits(account_num)
        for i in range(len(digit_list)-2, -1, -2):
            # double every other number
            digit_list[i] = sum(sep_digits(2*digit_list[i]))
        return sum(digit_list)
    # Return if the last digit matches the check digit (0 by default)
    return double_and_sum() % 10 == check_digit


"""
Implementation of the Luhn Algorithm using Pyrsistent data structures rather than standard structures
"""
def luhn_pyrsistent(account_num, check_digit: int = 0) -> bool:
    # Seperate number into a list.
    # Convert the number to a string, then iterate through string converting back to int at each item
    def sep_digits(n: int):
        return pvector(int(x) for x in str(n))

    # Double every other number in a list starting at the end of the list and sum the new total
    def double_and_sum() -> int:
        digit_list = sep_digits(account_num)

        # sum every number not being doubled
        even_sum = sum(digit_list[-1::-2])
        # double every other number
        # if the number being doubled is greater than 5, seperate the digits after doubling and sum those.
        odd_sum = sum(2*x if x < 5 else sum(sep_digits(2*x))for x in digit_list[-2::-2])
        return even_sum + odd_sum
    # Return if the last digit matches the check digit (0 by default)
    return double_and_sum() % 10 == check_digit


"""
# Coconut Implementation of Luhn Algorithm

from operator import mod

def luhn_algorithm(acc_num) = mod(evens+odds, 10) == 0 where:
    digits = digit_to_list(acc_num)
    evens = digits[-1::-2] |> sum
    odds = digits[-2::-2] |> fmap$(x -> sum(digit_to_list(x*2))) |> list |> sum

def digit_to_list(n) = str(n) |> map$(int) |> list

t1 = 79927398713  # True
t2 = 79927398714  # False

luhn_algorithm(t1) |> print
luhn_algorithm(t2) |> print
"""


def test_all():
    t1 = 79927398713  # True
    t2 = 79927398714  # False
    t3 = 1234567890123456  # False
    t4 = 1234567890123452  # True
    tests = [t1, t2, t3, t4]
    for f in [luhn_wiki, luhn_standard, luhn_pyrsistent]:
        print(f"\n{f.__name__}")
        for t in tests:
            print(f"Test on {t}: {f(t)}")


test_all()
