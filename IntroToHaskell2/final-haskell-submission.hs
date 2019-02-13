-- # # # # # # # # #   Question 1 - My Zip With  # # # # # # # # # --

-- by Jeffry

myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWith _ [] _ = []
myZipWith _ _ [] = []
-- not tail recursive
myZipWith f (x:xs) (y:ys) = (f x y) : myZipWith f xs ys
-- tail recursive, set up '. 
myZipWithTail' :: (a -> b -> c) -> [a] -> [b] -> [c] -> [c] 
myZipWithTail' _ [] _ orev = reverse orev
myZipWithTail' _ _ [] orev = reverse orev
myZipWithTail' f (x:xs) (y:ys) output = myZipWithTail' f xs ys $ f x y : output
myZipWithTail :: (a -> b -> c) -> [a] -> [b] -> [c]
myZipWithTail f (x:xs) (y:ys) = myZipWithTail' f (x:xs) (y:ys) []
-- tests
--myZipWith (*) [1,2,3] [1,2,3]
--myZipWithTail (*) [1,2,3] [1,2,3]




-- # # # # # # # # #   Question 2 - My Foldl # # # # # # # # # --

-- by Jeffry

-- takes in a f accumilator list 
-- iterates the f and returns the final accumilator, its reduce function on other languages
-- foldl traverses the list from left to right
-- myFoldl is tail recursive since once it finishes traversing the list, it will immediately return the total
myFoldl :: (a -> b -> b) -> b -> [a] -> b
myFoldl _ total [] = total
myFoldl f total (x:xs) = myFoldl f (f x total) xs 
-- test: myFoldl (+) 0 [1 .. 4], replace + with any operator




-- # # # # # # # # #   Question 3 - My Foldr  # # # # # # # # # --

-- by Soo

--3
--Recursive version
--Not tail recursive
myFoldr :: (a -> b -> b) -> b -> [a] -> b
myFoldr f accInit [] = accInit
myFoldr f acc (x:xs) = f x (myFoldr f acc xs)
--myFoldr (+) 0 [1 .. 4]
--10

--Reverse and foldl
myFlip [] = []
myFlip (x:xs) = (myFlip xs) ++ [x]

--myFoldr2 :: (a -> b -> b) -> b -> [a] -> b
myFoldr2 f accInit [] = accInit
myFoldr2 f acc xs = myFoldl2 f acc (myFlip xs)
myFoldl2 f accInit [] = accInit
myFoldl2 f acc (x:xs) = myFoldl2 f (f x acc) xs 

--myFoldr2 (+) 0 [1 .. 4]
--10




-- # # # # # # # # #   Question 4 - My Cycle  # # # # # # # # # --

-- by Adryel

{-

Question: Such a situation would produce an infinite loop in Java. Why doesn’t this lead
to an infinite loop in Haskell? Does it lead to an infinite loop in Python?

    It still produces an infinite list in Haskell, but since Haskell is lazy,
    it only evaluates as far as it needs to. Thus, while the list is infinite,
    Haskell will only look as far as it needs to to find the values it needs.
    Python is not lazy witb recursive evaluation, so a list function would need
    to terminate before the rest of the program to continue.


Question: What happens with the following? Explain why.
> cyc12 = myCycle [1,2]
-- Is this an infinite loop? What about Python? Why or why not?

    This is an infinite loop in Haskell but the implementation would need
    to be different in Python to allow the rest of the program to execute
    but retain the intended cycle.

> take 5 cyc12
-- Does this result in an infinite loop? What about Python? Why or why not?

    This does not result in an infinite loop in Haskell since the language
    is lazy. It only evaluates what it needs to.


Question: Walk through the step-by-step evaluation of
> take 5 cyc12

You may assume that take is implemented as follows
    take 0 _ = []
    take _ [] = []
    take n (x:xs) = x : take (n-1) xs

and that (++) is implemented as follows.
    [] ++ ys = ys
    (x:xs) ++ ys = x:(xs ++ ys)

For my purposes, I am defining myCycle as:
    myCycle :: [a] -> [a]
    myCycle x = x ++ myCycle x

>> cyc12 = myCycle [1,2]
>> take 5 cyc12
-> take 5 (cyc12 ++ myCycle cyc12)
-> take 5 ([1,2] ++ myCycle [1,2])
-> take 5 (1 : ([2] ++ myCycle [1,2]))
-> 1 : take 4 ([2] ++ myCycle [1,2])
-> 1 : take 4 (2 : ([] ++ myCycle [1,2]))
-> 1 : 2 : take 3 ([] ++ myCycle [1,2])
-> 1 : 2 : take 3 (myCycle [1,2])
-> 1 : 2 : take 3 ([1,2] ++ myCycle [1,2])
-> 1 : 2 : take 3 (1 : ([2] ++ myCycle [1,2]))
-> 1 : 2 : 1 : take 2 ([2] ++ myCycle [1,2])
-> 1 : 2 : 1 : take 2 (2 : ([] ++ myCycle [1,2]))
-> 1 : 2 : 1 : 2 : take 1 ([] ++ myCycle [1,2])
-> 1 : 2 : 1 : 2 : take 1 (myCycle [1,2])
-> 1 : 2 : 1 : 2 : take 1 ([1,2] ++ myCycle [1,2])
-> 1 : 2 : 1 : 2 : take 1 (1 : ([2] ++ myCycle [1,2]))
-> 1 : 2 : 1 : 2 : 1 : take 0 ([2] ++ myCycle [1,2])
-> 1 : 2 : 1 : 2 : 1 : []


** For a python equivalent of this operation, one would need to define a circular linked list for
** the operation to not end in an infinite loop


Question: Is there a Python equivalent [to using insertion sort to find the smallest element]?
If so, does it have the same time complexity?

    There is an equivalent in python, but the complexity would O(n^2) since python would not evaluate it lazily. The
    entire list would be sorted before pulling the first element.

-}




-- # # # # # # # # #   Question 5 - Compose  # # # # # # # # # --

-- by Soo

--5
-- h is type of (a -> c) 
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose g f = \x -> g ( f x )

--test5 = compose negate (*3)
--test5 5
-- - 15




-- # # # # # # # # #   Question 6 - Function Pairs  # # # # # # # # # --

-- by Jesus

{- 
   Question 6 - Function Pairs 
-}

{-
  For these functions, you can use either integers or floats

  All of these functions, when given a function, return a function which applies the given function
  on a list of elements, and returns a list of tuples. Each tuple follows the pattern where the first
  element is the element used to calculate the resultant when applied the given function, and the
  second element is that resultant.
  For example, if we assume that the function f() was given, then the tuple is as such: ( x , f(x) ),
  where x is an element from the given list. The resulting list, is a list of these structured tuples.
-}

-- ( Part a ) This is the function pairs implementation using the List Comprehension --
funcPairsList :: (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsList func list = [(x, func x) | x <- list]

-- ( Part B ) This is the function pairs implementation using the map function --
funcPairsMap :: (Eq a) => (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsMap func list = [(x,y) | x <- list, y <- map func list, y == func x ]

-- ( Part C )This is the function pairs implementation using both the zip and map functions --
funcPairsMapAndZip :: (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsMapAndZip func list = zip list $ map func list

-- ( Part D ) This is the function pairs implementation using the zipWith func, but not the map func --
funcPairsZipWith :: (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsZipWith func list = zipWith f list list
                                where f x _ = (x, func x)

-- ( Part E ) This is the function pairs implementation using the foldr function --
funcPairsFoldr :: (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsFoldr func list = foldr ( \x acc -> (x, func x) : acc ) [] list

-- ( Part F ) This is the function pairs implementation using the foldl function --
funcPairsFoldl :: (Num a) => (a -> a) -> [a] -> [(a, a)]
funcPairsFoldl func list = foldl ( \acc x -> acc ++ [(x, func x)] ) [] list

-- This function will be used for testing
sqrdPlus17 :: Num a => a -> a
sqrdPlus17 n = (n^2) + 17

-- Using the following functions for testing, type into ghci the line that is commented --
applyUsingList = funcPairsList sqrdPlus17
-- applyUsingList [1..8]

applyUsingMap = funcPairsMap sqrdPlus17
-- applyUsingMap [1..9]

applyUsingMapAndZip = funcPairsMapAndZip sqrdPlus17
-- applyUsingMapAndZip [1..10]

applyUsingZipWith = funcPairsZipWith sqrdPlus17
-- applyUsingZipWith [1..11]

applyUsingFoldr = funcPairsFoldr sqrdPlus17
-- applyUsingFoldr [1..12]

applyUsingFoldl = funcPairsFoldl sqrdPlus17
-- applyUsingFoldl [1..13]




-- # # # # # # # # #   Question 7 - While Loop  # # # # # # # # # --

-- by Jay

{-

Question: Is your while function tail recursive. Why or why not?

It is tail recursive, as the accumulator keeps updating at each recursive call of 
while and it does not have to wait till the last while call to evaluate the result.
At the final call, the final result is calculated by the result extractor and 
returned to the parent calls.

Question: Explain how nSquares works. What is the state? What do its components represent?

state is the accumulator on which the bodyFn performs the operation and returns the new
state. (index, list) is the form of state in this example. index keeps track of the iteration
count and list accumulates the results at each bodyFn operation.

For clarity, I will use following notations:
eval = (\(index, _) -> index <= n)
bodyFn = (\(index, list) -> (index + 1, index^2 : list))
extractRes = (reverse . snd)

> nSquares 15
while (1, []) eval bodyFn extractRes
while (bodyFn (1, [])) eval bodyFn extractRes

while (2, 1:[]) eval bodyFn extractRes
while (bodyFn (2, 1:[])) eval bodyFn extractRes

while (3, 2:1:[]) eval bodyFn extractRes
while (bodyFn (3, 2:1:[])) eval bodyFn extractRes

while (4, 3:2:1:[]) eval bodyFn extractRes
while (bodyFn (4, 3:2:1:[])) eval bodyFn extractRes

while (5, 4:3:2:1:[]) eval bodyFn extractRes
while (bodyFn (5, 4:3:2:1:[])) eval bodyFn extractRes
.
.
.
while (15, 14:13:12:11: ... :4:3:2:1:[]) eval bodyFn extractRes

while (bodyFn (15, 14:13:12:11: ... :4:3:2:1:[])) eval bodyFn extractRes
while (16, 15:14:13:12: ... :4:3:2:1:[]) eval bodyFn extractRes

extractRes (16, 15:14:13:12: ... :4:3:2:1:[])
reverse (15:14:13:12: ... :4:3:2:1:[])
reverse [15, 14, 13, ... , 3, 2, 1]
[1, 2, 3, ... , 13, 14, 15]

-}

-- While loop implementation
while :: state -> (state -> Bool) -> (state -> state) -> (state -> result) -> result
while state eval bodyFn extractRes
    | eval state = while (bodyFn state) eval bodyFn extractRes
    | otherwise = extractRes state


-- Test Example
nSquares:: Int -> [Int]
nSquares n =
    while (1, [])
          (\(index, _) -> index <= n) -- n is the nSquares argument.
          (\(index, list) -> (index + 1, index^2 : list))
          (reverse . snd) -- Extract the second element of
                          -- the tuple and reverse it.
-- test : nSquares 15 -> OP : [1,4,9,16,25,36,49,64,81,100,121,144,169,196,225]




-- # # # # # # # # #   Question 8 - While Loop & Function Pairs  # # # # # # # # # --

-- by Soo & Jeffry

myMap3 :: (a -> b) -> [a] -> [b]
myMap3 f xs =
    while (1, xs, [])
          (\(i, _, _) -> i <= n)
          (\(i, (x:xs), list) -> (i+1,xs, f x:list ))
          (\(_, _, list) -> reverse list)
    where n = length xs

-- test
-- main = do print $ myMap3 (+1) [1, 3 .. 15]

myWhileFoldl :: (b -> a -> b) -> b -> [a] -> b
myWhileFoldl f total xs = 
    while (1, xs, total)
          (\(i, _, _) -> i <= n)
          (\(i, (x:xs), total) -> (i+1,xs, f total x))
          (\(_, _, total) -> total)
    where n = length xs
    
-- main = do print $ myWhileFoldl (*) 1 [1, 2 .. 5]

--8 c
--Fibonacci number
nFibs n =
    while (1, 1, 1, [1, 1])
          (\(index, _, _, _ ) -> index <= (n - 2))
          (\(index, first, second, list) -> (index + 1, second, first + second, first + second : list))
          (\(_,_,_,list) -> reverse list )

--8 d
--Primes number
--8 d
--sieve of Eratosthenes

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

--next_state (nums, primes) = (filter (\x -> x `mod` (head nums) == 0)  nums, head nums : primes )