from pymonad import Just, Nothing, Maybe
from typing import Callable, Any
from functools import partial, reduce
from operator import and_


def safe_sqrt(x: float) -> Maybe:
    """
    Haskell:
        safeSqrt :: Double -> Maybe Double
        safeSqrt x
            | x < 0     = Nothing
            | otherwise = Just (sqrt x)
    """
    return Nothing if x < 0 else Just(x ** .5)


# test_safe_sqrt* takes the 4th root of a number by applying 'safe_sqrt' twice
def test_safe_sqrt0(x: float) -> Maybe:
    """
    Haskell:
        testSafeSqrt0 :: Double -> Maybe Double
        testSafeSqrt0 x = safeSqrt x >>= safeSqrt
    """
    return safe_sqrt(x) >> safe_sqrt


def test_safe_sqrt1(x: float) -> Maybe:
    """
    Haskell:
        testSafeSqrt1 :: Double -> Maybe Double
        testSafeSqrt1 x = do
                         y <- safeSqrt x
                         safeSqrt y
    """
    y = safe_sqrt(x)
    return safe_sqrt(y.getValue()) if y != Nothing else Nothing


def test_eqs(a, b):
    """
    Haskell:
        all :: Foldable t => (a -> Bool) -> t a -> Bool

        testEq0 a b = all (lambda x -> testSafeSqrt0 x == testSafeSqrt1 x) [a .. b]
        testEq1 a b = all id [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]
        testEq2 a b = foldl (&&) True [testSafeSqrt0 x == testSafeSqrt1 x | x <- [a .. b]]
    """
    eq1 = all((lambda x: test_safe_sqrt0(x) == test_safe_sqrt1(x))(i) for i in range(a, b))
    eq2 = all(test_safe_sqrt0(x) == test_safe_sqrt1(x) for x in range(a, b))
    eq3 = reduce(and_, [test_safe_sqrt0(x) == test_safe_sqrt1(x) for x in range(a, b)], True)
    return eq1 and eq2 and eq3


class Infix(object):
    def __init__(self, func):
        self.func = func

    def __ror__(self, other):
        return Infix(partial(self.func, other))

    def __rlshift__(self, other):
        """
        Reassigns the left shift operator (<<) if the left operand does not support
            the left shift operation with Infix
        e.g.
            self.__rlshift__(other) is called if other.__lshift__(self) returns NotImplemented.
        """
        return Infix(partial(self.func, other))

    def __rshift__(self, other):
        """
        Reassigns the right shift operator (>>)
        This applies the above partially applied function to the given parameter
        """
        return self.func(other)

    def __or__(self, other):
        return self.func(other)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


# Simple example use of Infix
@Infix
def add(x, y):
    return x + y


def demo_add():
    ex = 5 | add  # 5 | add  =  a partially applied function: add(5, _)
    print("5 | add =", ex)
    print("ex(6) =", ex(6))  # add(5,6)
    print("5 <<add>> 6  = ", 5 << add >> 6)  # add(5, 6) = 11
    # 5 << add >> 6  =  add(5,6)


@Infix
def bind(f1: Callable[[Any], Maybe], f2: Callable[[Any], Maybe]) -> Callable[[Any], Maybe]:
    """
    Effectively combines 2 'Maybe' functions into a new function that applies the
    result of the first into the second
    Haskell:
        (<.>) :: Monad m => (a -> m b) -> (b -> m c) -> (a -> m c)
        f1 <.> f2 = lambda x -> f1 x >>= f2

    Note:
        Pymonad defines right shift (>>) as its bind operand (>>=):
            (>>) = (>>=) :: Monad m => m b -> (b -> m c) -> m c
    """
    return lambda x: f1(x) >> f2


def safe_root(n: int) -> Callable[[float], Maybe]:
    """
    Haskell:
        safeRoot :: Int -> (Double -> Maybe Double)
        safeRoot n
            | n == 0 = Just
            | otherwise = safeSqrt <.> safeRoot (n-1)
    """
    return Just if n <= 0 else safe_sqrt << bind >> safe_root(n - 1)  # bind(safe_sqrt, safe_root(n-1))
    # example trace:  n = 1
    # Infix[safe_sqrt << bind  =  bind(safe_sqrt, _) ] >> (safe_root(0))
    # Infix( bind(safe_sqrt, _) ) >> (Just)  =  bind(safe_sqrt, Just)
    # returns lambda x: safe_sqrt(x) >> Just


def test_safe_root(n: int) -> Maybe:
    """
    Return 'Just 2' for any n >= 0
    Haskell:
        testSafeRoot :: Int -> Maybe Double
        testSafeRoot n = (safeRoot n) (2^(2^n))
    """
    return safe_root(n)(2**(2**n))


def test_safe_root_to9() -> bool:
    """
    Haskell:
        testSafeRootTo9 :: Bool
        testSafeRootTo9 = all (== Just 2) [testSafeRoot n | n <- [0 .. 9]]
    """
    return all(test_safe_root(n) == Just(2) for n in range(10))


demo_add()
print("\n\nTesting test_safe_sqrt0 and test_safe_sqrt1 (a=-2,b=4): ", test_eqs(-2, 4))
print("\n\nTest safe_root from 0->9 all equal Just(2): ", test_safe_root_to9())
