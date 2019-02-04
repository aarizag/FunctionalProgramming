{-
The assignment is to write a program to generates a sequence of numbers for which Goldbach’s other conjecture
does not hold. In other words, write programs that generate all non-prime odd numbers g so that for each there is no
prime p and integer k > 0 such that 
    g = p + 2 * k^2
-}

-- all Odd numbers starting from 3 -> 6000 for purposes for time trials
odd_nums :: [Integer]
odd_nums = [3,5 .. 6000]

-- all primes
primes :: [Integer]
primes = 2 : [p | p <- odd_nums, null (prev_primes p)]
    where prev_primes n = [d | d <- takeWhile (\x -> x^2 <= n) primes, n `mod` d == 0]

-- Receives a list of integers and checks if any one in the list is a perfect square
isASquare :: [Integer] -> Bool
isASquare [] = False
isASquare (item:rest) = if (nearest_root item)^2 == item then True else isASquare rest
    where nearest_root i = round $ sqrt $ fromInteger i

-- Checks if a number is Prime
isPrime :: Integer -> Bool
isPrime n = n `elem` (takeWhile (<=n) primes)

-- Compiles a list of numbers made by subtracting a number 'g' by every prime number smaller than it
g_test :: Integer -> [Integer]
g_test g = if isASquare [(g-p) `div` 2| p <- takeWhile (<g) primes] then [] else [g]

-- Iterates through a list of numbers and tests to see if they pass or fail Goldbach's Conjecture
-- Numbers that fail are added to a list and returned
g_iteration :: [Integer] -> [Integer]
g_iteration [] = []
g_iteration (g:remainder) = test ++ g_iteration remainder
    where test = if isPrime g then [] else g_test g

-- Tests Goldbach's Conjecture against a pre-defined list of odd numbers
goldbach_conjecture :: [Integer]
goldbach_conjecture = g_iteration odd_nums