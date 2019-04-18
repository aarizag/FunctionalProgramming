import Data.List

---------------------- Original ----------------------
--og_solveRPN :: String -> Double
--og_solveRPN = head . foldl _foldingFunction [] . words
--
--og_foldingFunction :: [Double] -> String -> [Double]
--og_foldingFunction (x:y:ys) "*" = (x * y):ys
--og_foldingFunction (x:y:ys) "+" = (x + y):ys
--og_foldingFunction (x:y:ys) "-" = (y - x):ys
--og_foldingFunction xs numberString = read numberString:xs



-------------------- Redone with Monads ---------------------
--foldM :: (Monad m) => (a -> b -> m a) -> a -> [b] -> m a
--foldM f a [] = return a -- Recall that &quot;return&quot;
---- wraps its argument.
--foldM f a (x:xs) = f a x >>= \fax -> foldM f fax xs
---- The variable fax receives the result of executing
---- f a x and then unwrapping the result.

readMaybe :: (Read a) => String -> Maybe a
readMaybe st = case reads st of [(x,"")] -> Just x
                                _ -> Nothing

--foldingFunction :: [Double] -> String -> Maybe [Double]
--foldingFunction (x:y:ys) "*" = return ((x * y):ys)
--foldingFunction (x:y:ys) "+" = return ((x + y):ys)
--foldingFunction (x:y:ys) "-" = return ((y - x):ys)
--foldingFunction xs numberString = liftM (:xs) (readMaybe numberString)

--solveRPN :: String -> Maybe Double
--solveRPN st = do
--    [result] <- foldM foldingFunction [] (words st)
--    return result

