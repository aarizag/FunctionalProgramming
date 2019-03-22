import time

"""
Sieve of Eratosthenes
Written by creating a recursive filter for every number in an infinite list of primes:
    The filter is a series of functions that determine if number is prime by seeing if it is divisible by none of
    the primes discovered thus far

All sieve functions return a list of n primes
"""


def infinite_odds() -> int:
    n = 1
    while True:
        n += 2
        yield n


def sieve(n: int) -> [int]:
    def f(func, n):
        return lambda x: None if x % n == 0 else func(x)

    nums = infinite_odds()
    primes = [2]
    filters = f(lambda x: x, 2)

    while True:
        nxt = next(nums)
        nxt = filters(nxt)

        if nxt is not None:
            primes += [nxt]
            filters = f(filters, nxt)

        if len(primes) >= n:
            return primes


def sieve2(n):
    from itertools import takewhile

    def fmod(modnum):
        def foo(x):
            return x if x % modnum != 0 else None
        foo.n = modnum
        return foo

    nums = infinite_odds()
    primes = [2]
    filters = [fmod(2)]

    while len(primes) < n:
        num = next(nums)

        for f in takewhile(lambda x: x.n*x.n <= num, filters):
            if f(num) is None:
                break
        else:
            primes += [num]
            filters += [fmod(num)]

    return primes


s = time.time()
p = sieve(500)
e = time.time()

s2 = time.time()
p2 = sieve2(50000)
e2 = time.time()

print(p[-1], '\n', e-s)  # 3571   0.11779046058654785 s
print(p2[-1], '\n', e2-s2)  # 104729   0.48451995849609375 s
                            # 611953   4.584943771362305 s

