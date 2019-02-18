import qualified Data.Map as M

{-
Simple Top Down recursive Fibonacci algorithm
-}
fib_top_down_rec n
        | n <= 2 = 1
        | otherwise = (fib_top_down_rec (n-1)) + (fib_top_down_rec (n-2))

{-
Simple Bottom up 'iterative' Fibonacci
-}
fib_bottom_up_iter(n) = fib 1 1 0
    where fib c ka kb
            | c < n = fib (c+1) (ka+kb) ka
            | otherwise = ka


{-
Generic Data Type for creating heterogeneous lists
S defines a string, I defines an Integer, and F defines an Integer.
F is used to distinguish between numbers in the sequence that
need to be broken down further and numbers that already have been added together.
-}
data Generic v = S {str :: String} | I {int :: Integer} | F {fibval :: Integer} deriving (Show, Eq)


{-
A dispatcher that uses pattern matching to distinguish between the
types of Generics
-}
dispatcher :: Generic v -> Char
dispatcher (S _) = 's'
dispatcher (I _) = 'i'
dispatcher (F _) = 'f'


{-
Top Down Iterative Fibonacci Algorithm

Takes no Parameters, but internally calls 'fib' which takes a list of Generics to represent commands and a
list of integers to represent a stack

Description of Guards:
    1st: Exit Condition - Determines if there are still inputs to be processed.
        Else return first int in stack
    2nd: If token is an Integer Generic, add it to stack and continue iterating through inputs
    3rd: Token Value needs to be broken down further:
        if it's 2 or 1, then append (Generic Int = 1) to inputs
        else append "+" symbol, then (Generic F = token-1 and token-2) to inputs
    4th: "+" causes the first 2 items in stack to be added together then appended to the input list
    otherwise: Fail safe, return -1 if none of the conditions are met. (Should never happen)

Description of where variables:
    token: The last item in the list of inputs. This determines the action to be taken
    inp: The list of inputs after "popping" off the last item.
    n: The integer value of a number to be broken down further in the fibonacci sequence
    first: the first integer in the stack
    second: the third item in the stack (jk it's the second)
    rest: the stack minus the first and second items
-}
fib_top_down_iter num_fibs = fib [F num_fibs] []
    where fib inputs stack
            | inputs == [] = head stack
            | dispatcher token == 'i' = fib inp (int token : stack)
            | dispatcher token == 'f' =
                if n <= 2 then fib (inp ++ [I 1]) stack
                else fib (inp ++ [S "+", F (n-1), F (n-2)]) stack
            | S "+" == token = fib (inp ++ [I (first+second)]) rest
            | otherwise = -1
                where token = last inputs
                      inp = init inputs
                      n = fibval token
                      (first:second:rest) = stack


{-
Top Down Iterative Fibonacci Algorithm with an optimization
"""
Same as fib_top_down_iter but with more efficient list processing.
Expands second recursive call down to the bottom.
"""
    - Abbott

Description is equal to the above function, but with the following changes:
    Guard 3: replaced the appending of n-1 and n-2 with a full iteration
        from n -> 2 with a step of -2. Since the iteration is guaranteed to
        end at 1 or 2, it will always prepend [1] to the stack.
    Guard 4: Rather than appending the value of the first and second numbers
        in the stack to the input list, it is added directly back to the stack
    variable list_iter: small function to iterate from n -> 2, creating a
        list of "+" symbols to add and numbers that need to be broken down
        further.
    variable n: removed
-}
fib_top_down_iter_with_opt_1 num_fibs = fib [F num_fibs] []
    where fib inputs stack
            | inputs == [] = head stack
            | dispatcher token == 'i' = fib inp $ int token : stack
            | dispatcher token == 'f' = fib (inp ++ (list_iter $ fibval token)) $ [1]++stack
            | S "+" == token = fib inp $ (first + second) : rest
            | otherwise = -1
                where token = last inputs
                      inp = init inputs
                      (first:second:rest) = stack
                      list_iter n
                        | n <= 2 = []
                        | otherwise = [S "+", F (n-1)] ++ list_iter (n-2)



{-
def fib_top_down_iter_with_opt_2(n, trace=False):
    if n <= 0:
        return 0
    if n == 2 or n == 1:
        return 1

    (inp, stack) = (['+', '*', 1, Fib(n), '*', 0, Fib(n-1)], [])

    while inp:
        [plus, times, ca, fib_a, _, cb, fib_b] = inp
        nx = fib_a.arg
        if nx == 2:
            break
        next_n = fib_b.arg - 1
        inp = [plus, times, ca+cb, fib_b, times, ca, Fib(next_n)]

    return ca + cb
-}

fib_top_down_iter_with_opt_2 num_fibs = fib [S "+", S "*", I 1, F num_fibs, S "*", I 0, F (num_fibs-1)]
    where fib inputs
            | num_fibs <= 2 = 1
            | inputs == [] || (nx == 2) = int ca + (int cb)
            | otherwise = fib next_inputs
                where (plus:times:ca:fib_a:_:cb:fib_b: empty) = inputs
                      nx = fibval fib_a
                      next_n = fibval fib_b - 1
                      next_inputs = (plus:times:I (int ca + (int cb)):fib_b:times:ca:(F next_n):[])





{-
Top Down Iterative Fibonacci Algorithm with Cache

Takes no Parameters, but internally calls 'fib' which takes a list of Generics to represent commands, a
list of integers to represent a stack, and a Map pre-made with the 1st and 2nd
Fibonacci numbers.

Description of Guards:
    1st: Exit Condition - Determines if there are still inputs to be processed.
        Else return first int in stack
    2nd: If token is an Integer Generic, add it to stack and continue iterating through inputs
    3rd: Token Value needs to be broken down further:
        Look up the value of the token in the cache (Data Map).
        If it exists, append that value (as a Generic) to the input list.
        Else append "cache", then "+" symbol, then (Generic F = token-1 and token-2) to inputs
    4th: "+" causes the first 2 items in stack to be added together then appended to the input list
    5th: "cache" determines that a new value in the Fibonacci sequence has been found and
        needs to be added to the cache. Insert the first and second values in the stack
        as a key value pair, respectively
    otherwise: Fail safe, return -1 if none of the conditions are met. (Should never happen)

Description of where variables:
    token: The last item in the list of inputs. This determines the action to be taken
    inp: The list of inputs after "popping" off the last item.
    n: The integer value of a number to be broken down further in the fibonacci sequence
    first: the first integer in the stack
    second: the third item in the stack (jk it's the second)
    rest: the stack minus the first and second items
-}
fib_top_down_iter_with_cache num_fibs = fib [F num_fibs] [] (M.fromList [(1,1),(2,1)])
    where fib inputs stack cache
            | inputs == [] = head stack
            | dispatcher token == 'i' = fib inp (int token : stack) cache
            | dispatcher token == 'f' =
                case M.lookup n cache of
                    Just x -> fib (inp++[I x]) stack cache
                    Nothing -> fib (inp ++ [S "cache", I n, S "+", F (n-1), F (n-2)]) stack cache
            | S "+" == token          = fib (inp ++ [I (first+second)]) rest cache
            | S "cache" == token      = fib inp (tail stack) (M.insert first second cache)
                where token = last inputs
                      inp = init inputs
                      n = fibval token
                      (first:second:rest) = stack
