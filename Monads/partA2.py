from pymonad import Nothing, Maybe, Just


class Expr:
    """
    Dummy superclass to support creation of 2 seperate constructors: Div and Val
    Meant to Replicate:
        data Expr = Val n | Div Expr Expr
    """
    pass


class Div(Expr):
    def __init__(self, a: Expr, b: Expr):
        self.a = a
        self.b = b


class Val(Expr):
    def __init__(self, n: int):
        self.n = n


def eval_basic(exp: Expr):
    """
    eval :: Expr -> Int
    eval (Val n) = n
    eval (Div a b) = eval a / eval b
    """
    if isinstance(exp, Val):
        return exp.n
    elif isinstance(exp, Div):
        return eval_basic(exp.a) // eval_basic(exp.b)


def safe_div(a: int, b: int) -> Maybe:
    """
    -- Division guarded against division by 0
    safe_div :: Int -> Int -> Maybe Int
    safe_div _ 0 = Nothing
    sage_div a b = Just (a/b)
    """
    return Nothing if b == 0 else Just(a // b)


def eval_do(exp: Expr) -> Maybe:
    """
    eval :: Expr -> Maybe Int
    eval (Val n) = return n
    eval (Div x y) = do n <- eval x
                        m <- eval y
                        safe_div n m
    """
    if isinstance(exp, Val):
        return Just(exp.n)
    elif isinstance(exp, Div):
        n = eval_do(exp.a).getValue()
        m = eval_do(exp.b).getValue()
        return safe_div(n, m) if n and m else None


def eval_non_do(exp: Expr) -> Maybe:
    """
        eval :: Expr -> Maybe Int
        eval (Val n) = return n
        eval (Div a b) = eval a >>= (\n -> eval b >>= (\m -> safe_div n m ))
    """
    if isinstance(exp, Val):
        return Just(exp.n)
    elif isinstance(exp, Div):
        return eval_non_do(exp.a) >> (lambda x: eval_non_do(exp.b) >> (lambda y: safe_div(x, y)))
        # Works similarly to the below, but abstracts the actual values from the 'Just' values
        # return (lambda x, y: safe_div(x,y))(eval_non_do(exp.a).getValue(), eval_non_do(exp.b).getValue())


# Test safe_div
x = safe_div(10, 2)
print(x)
print(x.getValue())

# Different expression tests
t1 = Div(Val(6), Val(2))  # 6 / 2 = 3
t2 = Div(Val(6), Val(0))  # 6 / 0 = Nothing
t3 = Div(Val(96), Div(Div(Val(72), Val(3)), Div(Val(9), Val(3))))  # 96 / [(72/3) / (9/3)] = 12

fs = [eval_do, eval_non_do]
ts = [t1, t2, t3]

# run tests in both functions
for f in fs:
    print(f"\n{f.__name__}")
    for t in ts:
        print(f"{f(t)}")
