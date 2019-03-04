toDigit :: Char -> Int
toDigit c = read [c]

toDigits :: Int -> [Int]
toDigits = map toDigit . show

doubleEveryOther :: [Int] -> [Int]
doubleEveryOther = zipWith (*) (cycle [1,2]) . reverse

sumDigits :: [Int] -> Int
sumDigits = sum . concat . map toDigits


checkSum :: Int -> Int
checkSum = sumDigits . doubleEveryOther . toDigits

isValid :: Int -> Bool

-- This simple version:
-- isValid n = checkSum n `mod` 10 == 0
-- can be tortured into this point-free form:
isValid = (==) 0 . (flip mod) 10 . checksum

-- Can you explain the point-free form?
-- (This is an exercise, not a claim that it’s better code.)
-- flip is defined in the Prelude, but it can be defined as follows.

myFlip :: (a -> b -> c) -> (b -> a -> c)
myFlip f = \x y -> f y x

testCC :: [Bool]
testCC = map isValid [1234567890123456, 1234567890123452]