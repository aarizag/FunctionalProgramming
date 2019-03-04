class Filter:
    def __init__(self, n):
        self.n = n

    def f(self, num: int):
        return None if num is None or num % self.n == 0 else num


def infinite_odds() -> int:
    n = 1
    while True:
        n += 2
        yield n

def sieve(n: int) -> [int]:
    nums = infinite_odds()
    primes = [2]
    filters = Filter(2).f

    while True:
        nxt = next(nums)
        # print(nxt)
        nxt = filters(nxt)
        # print(nxt)
        if nxt is not None:
            primes += [nxt]

            def m(x):
                return Filter(nxt).f(filters(x))
            filters = m

        if len(primes) >= n:
            return primes




import time

s = time.time()
p = sieve(5)
e = time.time()

print(p, '\n', e-s)