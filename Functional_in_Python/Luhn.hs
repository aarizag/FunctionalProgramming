{-
Author: Adryel Arizaga
Date: 2/24/19
No Rights Reserved tbh
-}


{-
Seperate Integer List
- Iterates through a list to ensure that all numbers are single digit
    - For every number in the list, seperate it into a list of its digits
- UNUSED
-}
sep_int_list :: [Integer] -> [Integer]
sep_int_list [] = []
sep_int_list (x:xs) = seperate_digits x ++ (sep_int_list xs)

{-
Seperate Digit* - translate a number into a list of its digits
    * tail recursive
-}
seperate_digits :: Integer -> [Integer]
seperate_digits num = sep num []
    where sep n accum_list
            | n <= 0 = accum_list
            | otherwise = sep d (m : accum_list)
                where (d, m) = divMod n 10

{-
Double Every Other - double every other number starting from the end
    e.g. [1,2,3,4,5] -> [1,4,3,8,5]
-}
double_every_other :: [Integer] -> [Integer]
double_every_other int_list = deo $ reverse int_list
    where
        deo [] = []
        deo (x:[]) = [x]
        deo (x0:x1:xs) = x0 : seperate_digits (2*x1) ++ deo xs

{-
Validate - Validate an "account number" via the Luhn algorithm (as written in the CSCI 490 problem set)
    1) Double the value of every second digit beginning from the right
       That is, the last digit is unchanged; the second-to-last is doubled; the third-to-last digit is unchanged;
       and so on
    2) Add the digits of the doubled values and the undoubled digits from the original number
       e.g. [2,3,16,6] -> 2+3+1+6+6 = 18
    3) If the resulting sum mod 10 is 0, the number is valid

    Example: validate 79927398713 = True
    Example: validate 79927398714 = False

Alternatively*, you can multiply the sum of the digits by some number and check the result against
a "check" number x (which is appended to the end of the account number).
    * Wikipedia
-}
validate :: Integer -> Bool
validate num = fin_val == 0
    where luhn_algorithm = sum . double_every_other . seperate_digits
          fin_val  = (luhn_algorithm num) `mod` 10

{-
4) Write a Haskell version of this elegant Python solution to the credit card problem:

from itertools import cycle
def myLuhn(n: int) -> bool:
    fn = lambda c: sum(divmod(2*int(c), 10))
    checksum = sum(f(c) for (f, c) in zip(cycle([int, fn]), reversed(str(n))))
    return checksum % 10 == 0
print(list(map(myLuhn, [1234567890123456, 1234567890123452])))
# => [False, True]
-}

-- Haskell's sum function seems to only consider the second element in a 2 element tuple
-- >>> sum (1,8)
-- 8
-- >>> sum [1,8]
-- 9
myLuhn n = sum [f x | (f, x) <- zip (cycle [\c -> c, fn]) digits] `mod` 10 == 0
    where fn = \c -> (\x -> fst x + snd x) $ divMod (2*c) 10
          digits  = reverse $ seperate_digits n