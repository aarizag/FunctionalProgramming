from typing import Callable, TypeVar, List, Union, Tuple, Any
from pymonad import Monad, Just, Maybe, Nothing
from operator import mul, add, sub

T1 = TypeVar('T1')
T2 = TypeVar('T2')


def foldM(f: Callable[[T1, T2], Monad], acc: T1, xs: List[T2]) -> Monad:
    """
    foldM :: (Monad m) => (a -> b -> m a) -> a -> [b] -> m a
    foldM f a [] = return a
    foldM f a (x:xs) = f a x >>= lambda fax -> foldM f fax xs
    """
    return Just(acc) if not xs else f(acc, xs) >> (lambda fax: foldM(f, fax, xs))

"""
readMaybe :: (Read a) => String -> Maybe a
readMaybe st = case reads st of [(x,"")] -> Just x
                                _ -> Nothing
"""
def read_maybe(item: str) -> Maybe:
    pass
    # return Just() if _ else Nothing


"""
foldingFunction :: [Double] -> String -> Maybe [Double]
foldingFunction (x:y:ys) "*" = return ((x * y):ys)
foldingFunction (x:y:ys) "+" = return ((x + y):ys)
foldingFunction (x:y:ys) "-" = return ((y - x):ys)
foldingFunction xs numberString = liftM(:xs)(readMaybe
numberString)
"""
def folding_function(xs: List[float], op: str) -> Maybe:
    operations = {"*": mul, "+": add, "-": sub}
    if xs:
        (x, y, *ys) = xs
        return Just((operations[op](x, y))+ys)

