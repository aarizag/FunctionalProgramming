import Debug.Trace

smallPrimeDivisors n = [d | d <- takeWhile (\x -> x^2 <= n) primes, n `mod` d == 0]
--primes = 2 : [n | n <- oddsFrom3, null (smallPrimeDivisors n)]
primes = 2 : [p | p <- oddsFrom3,
            let divisors = smallPrimeDivisors p,
            trace
                (show p ++ (if null divisors
                then "is prime"
                else "is divisible by" ++ show divisors) )
            null divisors
        ]

oddsFrom3 = [3, 5 .. ]

