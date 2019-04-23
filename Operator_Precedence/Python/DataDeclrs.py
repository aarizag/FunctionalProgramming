class ExprTree:
    def __eq__(self, other):
        return False


class Elmt:
    def __eq__(self, other):
        return False


class Optr:
    def __init__(self, f, c):
        self.f = f
        self.c = c

    def __eq__(self, other):
        return self.c == other.c


class ExprLeaf(ExprTree):
    def __init__(self, n):
        self.n = n

    def __str__(self):
        return self.n

    def __eq__(self, other):
        return self.n == other.n


class ExprNode(ExprTree):
    def __init__(self, tree1, optr, tree2):
        self.e1 = tree1
        self.op = optr
        self.e2 = tree2

    def __str__(self):
        return f"({self.e1},{[self.op.c]},{self.e2})"

    def __eq__(self, other):
        return self.e1 == other.e1 and self.op == other.op and self.e2 == other.e2


class Error(ExprTree):
    def __init__(self, elems: [Elmt]):
        self.elems = elems

    def __str__(self):
        return "Error"


class Nbr(Elmt):
    def __init__(self, num: int):
        self.num = num

    def __str__(self):
        return self.num

    def __eq__(self, other):
        return self.num == other.num


class LPar(Elmt):
    def __str__(self):
        return "("

    def __eq__(self, other):
        return True


class RPar(Elmt):
    def __str__(self):
        return ")"

    def __eq__(self, other):
        return True


class Op(Elmt):
    def __init__(self, func, c1, i, c2):
        self.f = func
        self.c1 = c1
        self.i = i
        self.c2 = c2

    def __str__(self):
        return [self.c1]

    def __eq__(self, other):
        return self.c1 == other.c1


class Expr(Elmt):
    def __init__(self, expr_tree: ExprTree):
        self.expr_tree = expr_tree

    def __str__(self):
        return self.expr_tree

    def __eq__(self, other):
        return self.expr_tree == other.expr_tree


def eval_expr(exp_tree: ExprTree) -> int:
    instance = {
        ExprLeaf: lambda e: e.n,
        ExprNode: lambda e: e.op(eval_expr(e.e1), eval_expr(e.e2)),
        Error: None
    }
    return instance[exp_tree.__class__](exp_tree)


def to_expr_tree(elem: Elmt) -> ExprTree:
    instance = {
        Nbr: lambda e: ExprLeaf(e.num),
        Expr: lambda e: e.expr_trees
    }
    return instance[elem.__class__](elem)


def wrapped_expr_tree(e1: Expr, e2: Op, e3: Expr) -> Elmt:
    return Expr(ExprNode(to_expr_tree(e1), Optr(e2.f, e2.c1), to_expr_tree(e3)))
