-- Problem 1
-- Create a function, using partial application of functions, that sees if a single Int is divisible by 5.
--  It takes in an Int and returns a Bool.

isFactorOf :: Int -> Int -> Bool
isFactorOf num1 num2 = num1 `mod` num2 == 0

factorOf5 :: Int -> Bool
factorOf5 num = isFactorOf num 5