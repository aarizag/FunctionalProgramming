module ParseStateClass (ParseState(..), trim) where

import DataDeclrs (Elmt(..), ExprTree(Error, ExprNode), Optr(..), toExprTree, wrappedExprTree) 

import Debug.Trace


-----------------------------------------------------------------------
-- The ParseState TypeClass. A TypeClass is like an Interface in Java.
-- Define a  ParseState  as supporting these functions. Also, require 
-- that every  ParseState  satisfies (i.e., implements)  Eq.
-----------------------------------------------------------------------

-- These functions will depend on the specific implementation
-- of a ParseState.
class Eq parseState => ParseState parseState where
  initialParseState :: [Elmt] -> parseState

  -- The parser uses a pair of lists to represent the parse progress.
  -- The lists should be understood as "facing each other," i.e.,
  -- the left list is in reverse order. The area to be reduced is
  -- at the start of the right list.
  --
  -- Each ParseState instance must be able to translate back and
  -- forth between such a pair of lists and its own ParseState
  -- representation.
  fromListPair :: ([Elmt], [Elmt]) -> parseState
  toListPair :: parseState -> ([Elmt], [Elmt])


  continueParse :: parseState -> Bool
  continueParse pState 
  -- For information about  <-  in a guard, see https://wiki.haskell.org/Pattern_guard
  -- or https://downloads.haskell.org/~ghc/5.02.3/docs/set/pattern-guards.html
    | ([], [_]) <- toListPair pState = False -- Successful parse. Stop.
    | (_,  [])  <- toListPair pState = False -- Failed parse. Stop.
    | otherwise                      = True  -- Unfinished parse. Continue.
  



  -- The following functions are implementation-independent 
  -- and can be used by all  ParseState  instances.
  parse :: [Elmt] -> parseState  
  parse tokens = 
    let initialPState = initialParseState tokens
    in perhapsTrace ("\n       " ++ showParseState initialPState) $
                 while initialPState continueParse parseAStep

  parseAStep :: parseState -> parseState
  parseAStep pState = 
    let newState = 
            case toListPair pState of
            (left, []) -> fromListPair (left, [])
            (left, right)   -> 
              let updatedRight = applyARule right 
              in slideWindow (if updatedRight /= right then (-3) else 1) 
                             $ fromListPair (left, updatedRight)
    in perhapsTrace ("       "  ++ showParseState newState) 
                 newState    
                    

  pStateToETree :: parseState -> ExprTree  
  pStateToETree pState = 
          case toListPair pState of
          ([], [expr]) -> toExprTree expr
          (exprs, [])  -> Error $ reverse exprs


  
  showParseState :: parseState -> String
  showParseState pState = 
    let (left, windowAndRight) = toListPair pState  
        (window, right) = splitAt 5 windowAndRight
    in                (trim . show . reverse) left 
       ++ "   << " ++ (replace "," ", " . trim . show) window ++ " >>     " 
       ++             (trim . show) right


  slideWindow :: Int -> parseState -> parseState
  slideWindow n pState
    | n < 0  = -- Since n < 0, length left + n < length n
        let (shifted, left')  = splitAt (-n) left 
        in -- trace ((show . reverse) shifted ++ " " ++ (show . reverse) left') $ 
                 fromListPair (left', reverse shifted ++ right)
    | n == 0 = pState
    | n > 0  = 
        let (shifted, right') = splitAt n right
        in fromListPair (reverse shifted ++ left, right') 
    where (left, right) = toListPair pState                             


-- --------------------------------------------------------------------
-- -- Utility functions used by ParseState functions.
-- --------------------------------------------------------------------


applyARule :: [Elmt] -> [Elmt]
-- For information about  <-  in a guard, see https://wiki.haskell.org/Pattern_guard
-- or https://downloads.haskell.org/~ghc/5.02.3/docs/set/pattern-guards.html

-- What does this rule do?
applyARule right
  | ([LPar, e, RPar], rest) <- splitAt 3 right
  , isOperand e  = e:rest

-- What does this rule do?
applyARule right
  | ([op1, e1, op, e2, op2], rest) <- splitAt 5 right
  , isOperand e1 && isOperator op && isOperand e2
  , higherPrec op1 op op2 
      = let (Op fn char _ _) = op
        in [op1, Expr (ExprNode (toExprTree e1) (Optr fn char) (toExprTree e2)), op2] 
           ++ rest

-- Why is this defined?
applyARule right = right


higherPrec :: Elmt -> Elmt -> Elmt -> Bool  
higherPrec leftOp op rightOp =
  higherPrecThanLeft leftOp op && higherPrecThanRight op rightOp  


higherPrecThanLeft :: Elmt -> Elmt -> Bool
higherPrecThanLeft LPar          _     = True
higherPrecThanLeft (Op _ _ p0 a0) (Op _ _ p1 a1) 
  | p0 < p1                            = True
  | p0 == p1 && a0 == 'R' && a1 == 'R' = True
higherPrecThanLeft _             _     = False
  

higherPrecThanRight :: Elmt -> Elmt -> Bool
higherPrecThanRight _             RPar = True
higherPrecThanRight (Op _ _ p1 a1) (Op _ _ p2 a2) 
  | p1 > p2                            = True
  | p1 == p2 && a1 == 'L' && a2 == 'L' = True
higherPrecThanRight _             _    = False


isOperand :: Elmt -> Bool
isOperand (Nbr _)  = True
isOperand (Expr _) = True
isOperand _        = False

isOperator :: Elmt -> Bool
isOperator (Op _ _ _ _)  = True
isOperator _             = False


replace :: Eq a => [a] -> [a] -> [a] -> [a]
replace xs ys zs 
  | (start, rest) <- splitAt (length xs) zs
  , start == xs = ys ++ replace xs ys rest
  | w:ws <- zs  = w : replace xs ys ws
  | null zs     = []


trim :: String -> String
trim (x:rest) | x `elem` "([" = init rest
trim str        = str


while :: state -> (state -> Bool) -> (state -> state) -> state
while state continueTest bodyFn = wh state
  -- The auxiliary function is not necessary. Defining it just
  -- avoids repeatedly passing  continueTest  and  bodyFn.
  where 
    wh st
      | continueTest st = wh (bodyFn st)
      | otherwise       = st 


-- ---------------------------------------------------------
--  Trace stuff
-- ---------------------------------------------------------

perhapsTrace :: String -> a ->  a
perhapsTrace str e =  case shouldTrace of
                      True  -> trace str e
                      False -> e 
  where shouldTrace = False 
                     