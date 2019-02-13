# importing the libraries and packages used
from typing import List, Tuple, Sequence, Any, Callable, TypeVar, Union
from functools import reduce
import doctest


""" # # # # # # # # #   Question 1 - My Zip With  # # # # # # # # # """

# by Jeffry

# Question: If you use recursion, does the order of the clauses matter? Why or why not?

    # -----------------> Unanswered. <----------------- #


T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
# myZipWith :: (a -> b -> c) -> [a] -> [b] -> [c]
# haskell code: myZipWith f (x:xs) (y:ys) = (f x y) : myZipWith f xs ys
def myZipWith (f: Callable[[T1,T2], T3], xs: Sequence[T1], ys: Sequence[T2]) -> Sequence[T3] : 
    """
    >>> myZipWith(lambda x, y: x + y, [1,2,3], [2,2,2])
    [3, 4, 5]
    """
    # what about map(f, xs, ys)
    return [f(x, y) for x, y in zip(xs, ys)]




""" # # # # # # # # #   Question 2 - My Foldl  # # # # # # # # # """

# by Jeffry

# Question: 
# Is this tail recursive. Why or why not?

    # myFoldl is tail recursive since once it finishes traversing the list, it will 
    # immediately return the total

# Question: 
# What is the relationship between the value produced by the base case and
# the initial function call? That is, assume you make a call like this:
# > myFoldl fn accInit list
# and assume that when the base case is reached it returns value
# What is the relationship (if any) between value and myFoldl fn accInit list?

    # -----------------> Unanswered. <----------------- #


# myFoldl :: (a -> b -> b) -> b -> [a] -> b
# myFoldl f total (x:xs) = myFoldl f (f x total) xs
# recursion here is not tail recursive
def myFoldlN (f: Callable[[T1,T2], T2], total: T2, xs: Sequence[T1]) -> T2 : 
    """
    >>> myFoldlN(lambda x, y: x * y, 1, [1,2,3,4])
    24
    """
    if(xs):
        return myFoldl(f, f(xs[0], total), xs[1:])
    else: 
        return total

# tail recursive:
# update the total as we iterate through the xs list, return the total after we are done
def myFoldl (f: Callable[[T1,T2], T2], total: T2, xs: Sequence[T1]) -> T2 : 
    """
    >>> myFoldl(lambda x, y: x * y, 1, [1,2,3,4])
    24
    """
    for x in xs:
        total = f(x, total)
    return total




""" # # # # # # # # #   Question 3 - My Foldr  # # # # # # # # # """

# by Soo

# Question: 
# Is this tail recursive. Why or why not?

    # -----------------> Unanswered. <----------------- #

# Question: 
# What is the relationship between the value produced by the base case
# and the initial accumulator value in the initial function call?

    # -----------------> Unanswered. <----------------- #

def f(f: Callable[[Any, Any], Any], x, y):
    return f(x, y)

def head(xs: Sequence) -> Any:
    return xs[0] if len(xs) > 0 else []

def tail(xs: Sequence) -> Any:
    return xs[1:] if len(xs) > 0 else []

def last(xs: Sequence) -> Any:
    return xs[-1] if len(xs) > 0 else []

def rest(xs: Sequence) -> Any:
    return xs[:-1] if len(xs) > 0 else []

def myFold1(func: Callable[[Any, Any], Any], acc, xs: Sequence) -> Any:
    """
    :param func:
    :param acc:
    :param xs:
    :return:
    >>> myFold1((lambda x, y: x - y), 0, [1, 2, 3])
    -6
    """
    return acc if len(xs) <= 0 else \
        f(func, acc, head(xs)) if len(xs) == 1 else \
        myFold1(func, f(func, acc, head(xs)), tail(xs))

def myFoldr(func: Callable[[Any, Any], Any], acc, xs: Sequence) -> Any:
    """
    :param func:
    :param acc:
    :param xs:
    :return:
    >>> myFoldr((lambda x, y: x - y), 0, [1, 2, 3])
    0
    """
    return acc if len(xs) <= 0 else \
        f(func, last(xs), acc) if len(xs) == 1 else \
        myFold1(func, f(func, last(xs), acc), rest(xs))

def myFoldr2(func: Callable[[Any, Any], Any], acc, xs: Sequence) -> Any:
    """

    :param func:
    :param acc:
    :param xs:
    :return:
    >>> myFoldr2((lambda x, y: x - y), 0, [1, 2, 3])
    0
    """
    return myFold12(func, acc , xs.reverse())

def myFold12(func: Callable[[Any, Any], Any], acc, xs: Sequence) -> Any:
    return acc if xs is None else \
        f(func, head(xs), acc) if len(xs) == 1 else \
        myFold12(func, f(func, head(xs), acc), tail(xs))




""" # # # # # # # # #   Question 4 - My Cycle  # # # # # # # # # """

# by Adryel

"""

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

"""



""" # # # # # # # # #   Question 5 - Compose  # # # # # # # # # """

# by Soo

# Question: 
# Given g :: b -> c, f:: a -> b, and h = g `compose` f,
# what is the type of h? (Hint: the type of h is not the same as the type of compose.)

    # h is type of (a -> c)

# --5
# compose :: (b -> c) -> (a -> b) -> (a -> c)
# compose g f = \x -> g ( f x )
# --test5 = compose negate (*3)
# --test5 5
# -- - 15

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def compose(g: Callable[[B],C], f: Callable[[A],B], x) -> C:
    """
    :param g:
    :param f:
    :param x:
    :return:
    >>> compose((lambda x: -x),(lambda x: x*3),5)
    -15
    """
    return g(f(x))




""" # # # # # # # # #   Question 6 - Function Pairs  # # # # # # # # # """

# by Jesus

# In the following functions it was assumed that we were dealing with integers; although floats could
# also be used, it was assumed that we used integers only in order to simplify the type annotations

# All of these functions, when given a function, return a function which applies the given function
# on a list of elements, and returns a list of tuples. Each tuple follows the pattern where the first
# element is the element used to calculate the resultant when applied the given function, and the
# second element is that resultant.
# For example, if we assume that the function f() was given, then the tuple is as such: ( x , f(x) ),
# where x is an element from the given list. The resulting list, is a list of these structured tuples.

# The abbreviation 'fp' stands for function pairs

# ( Part a ) This is the function pairs implementation using the List Comprehension
def fp_list(func: Callable[[int], int]) -> Callable[[List[int]], List[Tuple[int, int]]]:
    """
    >>> apply_using_list = fp_list(sqrd_plus_17)
    >>> apply_using_list(range(9))
    [(0, 17), (1, 18), (2, 21), (3, 26), (4, 33), (5, 42), (6, 53), (7, 66), (8, 81)]
    """
    def func_on_list(a_list: List[int]) -> List[Tuple[int, int]]:
        return [ (x, func(x)) for x in a_list ]
    return func_on_list

# ( Part B ) This is the function pairs implementation using the map() function
def fp_map(func: Callable[[int], int]) -> Callable[[List[int]], List[Tuple[int, int]]]:
    """
    >>> apply_using_map = fp_map(sqrd_plus_17)
    >>> apply_using_map(range(10))
    [(0, 17), (1, 18), (2, 21), (3, 26), (4, 33), (5, 42), (6, 53), (7, 66), (8, 81), (9, 98)]
    """
    def func_on_list(a_list: List[int]) -> List[Tuple[int, int]]:
        result: List[int] = list( map(func, a_list) )
        return [ (a_list[i] , result[i]) for i in range(len(a_list)) ]
    return func_on_list

# ( Part C )This is the function pairs implementation using both the zip() and map() functions
def fp_zip_and_map(func: Callable[[int], int]) -> Callable[[List[int]], List[Tuple[int, int]]]:
    """
    >>> apply_using_zip_and_map = fp_zip_and_map(sqrd_plus_17)
    >>> apply_using_zip_and_map(range(11))
    [(0, 17), (1, 18), (2, 21), (3, 26), (4, 33), (5, 42), (6, 53), (7, 66), (8, 81), (9, 98), (10, 117)]
    """
    def func_on_list(a_list: List[int]) -> List[Tuple[int, int]]:
        result: List[int] = list( map(func, a_list) )
        return [ x for x in zip(a_list, result) ]
    return func_on_list

# ( Part D ) This is the function pairs implementation using the zip() function, but not the map() function
def fp_zip_no_map(func: Callable[[int], int]) -> Callable[[List[int]], List[Tuple[int, int]]]:
    """
    >>> apply_using_only_zip = fp_zip_no_map(sqrd_plus_17)
    >>> apply_using_only_zip(range(12))
    [(0, 17), (1, 18), (2, 21), (3, 26), (4, 33), (5, 42), (6, 53), (7, 66), (8, 81), (9, 98), (10, 117), (11, 138)]
    """
    def func_on_list(a_list: List[int]) -> List[Tuple[int, int]]:
        result: List[int] = [ func(r) for r in a_list  ]
        return [ x for x in zip(a_list, result) ]
    return func_on_list

# ( Part E & F ) This is the function pairs implementation using the 
# reduce() function; the Python-equivalent foldl function from Haskell
def fp_reduce(func: Callable[[int], int]) -> Callable[[List[int]], List[Tuple[int, int]]]:
    """
    >>> apply_using_reduce = fp_reduce(sqrd_plus_17)
    >>> apply_using_reduce(range(13))
    [(0, 17), (1, 18), (2, 21), (3, 26), (4, 33), (5, 42), (6, 53), (7, 66), (8, 81), (9, 98), (10, 117), (11, 138), (12, 161)]
    """
    def func_on_list(a_list: List[int]) -> List[Tuple[int, int]]:
        return reduce( ( lambda x,y: x + [ ( y , func(y) ) ] ) , a_list , [] )
    return func_on_list

# This is a function that I will use for testing.
# It is the function that will be passed as a parameter to the above functions.
def sqrd_plus_17(n):
    """
    >>> sqrd_plus_17(25)
    642
    """
    return (n ** 2) + 17




""" # # # # # # # # #   Question 7 - While Loop  # # # # # # # # # """

# by Jay

"""

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

"""

State = TypeVar('State')
Result = TypeVar('Result')

# While loop implementation
def while_(state: State, evalFn: Callable[[State], bool] , bodyFn: Callable[[State], State], extractRes: Callable[[State], Result]) -> Result:
    return while_(bodyFn(state), evalFn, bodyFn, extractRes) if evalFn(state) else extractRes(state)

# Test Example
def nSquares(n: Union[int, float]) -> [int]:
    return while_(
            (1, []),
            lambda state: state[0] <= n,
            lambda state: (state[0]+1, state[1]+[state[0]**2]),
            lambda state: state[1]
        )
print(nSquares(15.1))



""" # # # # # # # # #   Question 8 - While Loop & Function Pairs # # # # # # # # # """

# by ?





# This is used to run the tests written in the doc strings
if __name__ == '__main__':
    doctest.testmod(verbose=True)

    # print(functionPairs_a((lambda x: x*x),range(1,5)))
    # print(functionPairs_b((lambda x: x * x), range(1, 5)))
    # print(functionPairs_c((lambda x: x * x), range(1, 5)))
    # print(functionPairs_d((lambda x: x * x), range(1, 5)))

    # test5 = compose((lambda x: -x),(lambda x: x*3), 5)
    # print(test5)
    # print(myFold1(operator.sub, 0, [1, 2, 3]))
    # print(myFold1((lambda x, y : x - y), 0, [1,2,3]))
    # print(myFoldr(operator.sub, 0, [1, 2, 3]))
    # print(myFoldr2(operator.sub, 0, [1, 2, 3]))