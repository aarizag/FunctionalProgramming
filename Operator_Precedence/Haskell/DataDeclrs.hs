module DataDeclrs 
( Elmt(..)  -- Export all the  Elmt  constructors.
, evalExpr
, ExprTree(Error, ExprNode)
, Optr(..)
, toExprTree
, wrappedExprTree
) where 


---------------------------------------------------------------------
-- Data declarations.
---------------------------------------------------------------------

-- These are elements in the sequence to be (and being) parsed.
data Elmt =   Nbr Int 
            | LPar
            | RPar
            | Op (Int -> Int -> Int) Char Int Char
            | Expr ExprTree


-- These are constructors for the parse Tree. During 
-- the parse they are wrapped in Expr elements
data ExprTree =   ExprLeaf Int 
                | ExprNode ExprTree Optr ExprTree
                | Error [Elmt] 


-- Represents operators in the parse tree. 
data Optr = Optr (Int -> Int -> Int) Char


evalExpr :: ExprTree -> Int
evalExpr (ExprLeaf n) = n
evalExpr (ExprNode e1 (Optr op _) e2) =  (evalExpr e1) `op` (evalExpr e2) 
evalExpr (Error elmts) = -1 -- Would prefer NaN, but it's not an Int.


toExprTree :: Elmt -> ExprTree
toExprTree (Nbr n) = ExprLeaf n
toExprTree (Expr exprTree) = exprTree 


wrappedExprTree :: Elmt -> Elmt -> Elmt -> Elmt
wrappedExprTree e1 (Op fn char _ _) e2 =
  Expr (ExprNode (toExprTree e1) (Optr fn char) (toExprTree e2))


instance Show Elmt where  
    show LPar            = "("
    show RPar            = ")"
    show (Nbr n)         = show n
    show (Op _ c _ _)    = [c] -- Assume every operator is one character.
    show (Expr exprTree) = show exprTree

instance Show ExprTree where  
    show (ExprLeaf n)   = show n
    show (ExprNode e1 (Optr _ c) e2) 
                       = concat["(", show e1, [c], show e2, ")"] 
    show (Error elmts) = 
        "Error:" ++ tail (foldr (\s acc -> ", " ++ show s ++ acc) "" elmts)

instance Eq Elmt where
    Nbr n1         == Nbr n2       = n1 == n2
    LPar           == LPar         = True  
    RPar           == RPar         = True  
    Op _ c1 _ _    == Op _ c2 _ _  = c1 == c2
    Expr exprTree1 == Expr exprTree2
                                   = exprTree1 == exprTree2 
    _            == _              = False       

instance Eq ExprTree where
    ExprLeaf n1 == ExprLeaf n2 = n1 == n2
    ExprNode e11 optr1 e12 == ExprNode e21 optr2 e22
                               =    e11   == e21 
                                 && optr1 == optr2 
                                 && e12   == e22 
    _          == _            = False       


instance Eq Optr where
    (Optr _ c1) == (Optr _ c2) = c1 == c2                     


