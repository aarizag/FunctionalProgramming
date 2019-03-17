toDigit_  :: Char -> Int
toDigit_  = read . (:[])

doubleAndSum :: [Int] -> Int
doubleAndSum = snd . foldr (\i (atEvnPos, acc) -> (not atEvnPos, nextVal atEvnPos i + acc)) (False, 0)
    where
        nextVal:: Bool -> Int -> Int
        nextVal True i = (uncurry_  (+) . (`divMod` 10) . (*2)) i
        nextVal False i = i
        
uncurry_  :: (t2 -> t1 -> t) -> (t2, t1) -> t
uncurry_  f = \(x, y) -> f x y

myLuhn :: Int -> Bool
myLuhn = (0 ==) . (`mod` 10) . doubleAndSum . map toDigit_  . show

testCC_  :: [Bool]
testCC_  = map myLuhn [1234567890123456, 1234567890123452]
-- => [False, True]