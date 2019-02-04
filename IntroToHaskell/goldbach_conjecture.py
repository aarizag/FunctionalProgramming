from itertools import takewhile
from math import sqrt
import time


"""
@:name: find_primes
@:desc: Return a list of primes that ends at the next prime past the "max" param
@:returns: list of primes (integers)
@:keyword: 
    max - an integer that denotes the value that must be smaller than the largest prime
        @default: 2^13 (8192)
    primes - list of primes that have been previously evaluated
        @default: None
"""
def find_primes(max: int = 2**13, primes: [int] = None) -> [int]:
    if not primes or primes == [2]:
        primes = [2, 3]  # default first 2 primes instead of just 2 to protect iteration later

    if primes[-1] > max:  # Lazy evaluation: if there exists a prime larger than the max, just return the list
        return primes

    _primes = primes.copy()  # create a new list instead of modifying the original
    i: int = _primes[-1]  # start iterating at the max prime value

    while _primes[-1] < max:
        i += 2  # this would fail if primes = [2]
        check = True
        for p in _primes:
            if i % p == 0:
                check = False
                break
        if check:
            _primes += [i]

    return _primes


"""
@:name: is_prime
@:desc: check if a given number is prime by evaluating if it exists within a list of primes
        Function exists for readability, but can be replaced by lambda function:
            # is_prime = lambda x: x in primes
@:returns: boolean
@:param:
    num - number being checked
    primes - list of primes
"""
def is_prime(num: int, primes: [int]) -> bool:
    return num in primes


"""
@:name: is_a_square
@:desc: checks if number is a perfect square
@:returns: boolean
@:param:
    num - integer to be checked
"""
def is_a_square(num: int) -> bool:
    return round(sqrt(num))**2 == num


"""
@:name: conjecture_test
@:desc: perform a test to check for exceptions to Goldbach's conjecture, namely
        for all non-prime odd numbers g so that for each there is a prime p and integer k > 0 such that 
            g = p + 2 * k^2
@:returns: an empty list if the condition is met, the number 'g' in a list otherwise
@:param:
    g - integer to be checked
    primes - list of evaluated prime numbers
"""
def conjecture_test(g: int, primes: [int]) -> [int]:
    # Taking advantage of the lazy evaluation of find_primes, primes will only ever have one element larger than g,
    # so we can speed up the evaluation by simply grabbing the primes we need with indexing.
    # If using a pre-loaded, large list of primes, use:
    #   takewhile((lambda x: x < g), primes)
    # in the place of
    #   primes[-1]
    for p in primes[:-1]:
        if is_a_square((g-p)//2):
            return []
    return [g]


"""
@:name: goldman_conjecture
@:desc: check all non-prime odd numbers in the given range to check if they satisfy Goldbach's Conjecture
@:returns: None
@:keyword: 
    max_test - the maximum number to be tested against the conjecture
    primes - a list of prime integers that have already been evaluated
"""
def goldbach_conjecture(max_test: int = 6000, primes: [int] = None) -> None:
    odd_nums: [int] = [i for i in range(3, max_test, 2)]  # Odd numbers 3 -> 10000
    exceptions: [int] = []  # list of exceptions to the conjecture

    for odd_num in odd_nums:
        primes = find_primes(odd_num, primes)
        if not is_prime(odd_num, primes):  # only check non-prime odd numbers
            exceptions += conjecture_test(odd_num, primes)

    print(exceptions)


start = time.time()
goldbach_conjecture()
total = time.time() - start
print(total)