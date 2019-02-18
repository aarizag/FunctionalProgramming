while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state eval bodyFn extractRes
    | eval state = while (bodyFn state) eval bodyFn extractRes
    | otherwise = extractRes state


n_primes n =
    while ((2:[3,5..]), [], 0)
          (\(_, _, ind) -> n > ind)
          (\(nums, primes, ind) -> (filter (\x -> x `mod` (head nums) /= 0)  nums, head nums : primes, ind+1 ))
          (\(_,primes, _) -> reverse primes)


          
smallPrimeDivisors n primes = [d | d <- primes, n `mod` d == 0]
isPrime n primes = null (smallPrimeDivisors n primes)

nextPrime p primes
          | isPrime p primes = p
          | otherwise = nextPrime (p + 1) primes

nPrimes n =
        while (1, 2, [])
            (\(index, _, _) -> index <= n)
            (\(index, p, list) -> (index + 1, (nextPrime p list), (nextPrime p list) : list))
            (\(_, _, list) -> reverse list)