
class goldbach:
    def __init__(self):
        from math import sqrt
        from itertools import takewhile
        self.primes = [2, 3]
        self.sqrt = sqrt
        self.takewhile = takewhile

    def next_prime(self, floor):
        i = floor if floor % 2 == 1 else floor - 1
        while self.primes[-1] < floor:
            for p in self.takewhile((lambda x: x < self.sqrt(i)), self.primes):
                if i % p == 0:
                    break
            else:
                self.primes += [i]
            i += 2

    def is_prime(self, num):
        return num in self.primes

    def is_perfect_square(self, num):
        return round(self.sqrt(num))**2 == num

    def conjecture_test(self, g: int) -> [int]:
        for p in self.primes[:-1]:
            k = (g - p) // 2
            if self.is_perfect_square(k):
                return None
        return g

    def generate_odds(self):
        n = 3
        while True:
            yield n
            n += 2

    def iterate_test(self):
        exceptions: [int] = []  # list of exceptions to the conjecture
        odd_nums = self.generate_odds()
        while len(exceptions) < 2:
            o = next(odd_nums)
            self.next_prime(o)
            exceptions += [o] if not self.is_prime(o) and self.conjecture_test(o) else []
        return exceptions


import time
total = 0
for i in range(10):
    start = time.time()
    exceptions = goldbach().iterate_test()
    total += time.time() - start

print("Average time taken after 10 runs:", (total/10))
print("Exceptions found:", exceptions)