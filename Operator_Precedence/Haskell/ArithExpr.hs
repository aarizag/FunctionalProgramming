module ArithExpr where

import DataDeclrs (Elmt, ExprTree, evalExpr)
import ParseStateClass (parse, pStateToETree, trim)
import ParseState_V1Type (ParseState_V1)
import Tokenizer (tokenize)


evalArith :: String -> (String, ExprTree, Int) 
evalArith string = let tokenList = tokenize string
                       pState    = (parse tokenList) :: ParseState_V1
                       exprTree  = pStateToETree pState
                       value     = evalExpr exprTree
                   in (string, exprTree, value)



-------------------------------------------------------------------
-- ArithExpr Tests
-------------------------------------------------------------------

showResult :: (String, ExprTree, Int) -> String
showResult (str, exprTree, val) = 
     "     " ++ show str 
  ++ " --> " ++ (trim . show) exprTree -- Strip outer parentheses
  ++ " --> " ++ show val

                            
testCases :: [String]        
testCases = [ "8-4-2"           --    2
            , "(8-4)-2"         --    2
            , "8-(4-2)"         --    6
            , "8/4/2"           --    1
            , "(8/4)/2"         --    1
            , "8/(4/2)"         --    4
            , "2^3^2"           --  512
            , "(2^3)^2"         --   64
            , "2^(3^2)"         --  512
            , "16-7-3*2^2"      --   -3
            , "3*4+5^2"         --   37            
            , "6-3*2"           --    0       
            , "6*3-2"           --   16      
            , "6*(3-1)"         --   12      
            , "6-3*(1-7)"       --   24      
            , "(6-3)*2"         --    6       
            , "1100-34-2*2^3^2" --   42     
            , "2^3^2*2-27-100"  --  897   
            , "5+(6-3)^2+5"     --   19      
            , "3+4/(6-4)^2"     --    4        
            , "3+4/6-4^2"       --  -13      
            , "2^(6-3)^2"       --  512    
            , "2^6-3"           --   61      
            , "(6-3)^2"         --    9       
            , "16-3^2"          --    7       
            , "3"               --    3 
            , "3+4/6-4*5"       --  -17
            , "3+4/6-+4*5^2"    --  Error: (, (3+(4/6)), -, +, (4*(5^2)), )
                                --   -1
            , "3+4/6-4 7*5"     --  Error: (, (3+(4/6)), -, 4, 7, *, 5, )
                                --   -1
            ]    


testArithExprs :: IO ()
testArithExprs = 
  let strings = map (showResult . evalArith)  testCases
  in putStr . unlines $ "   Input string --> Tree --> Value" : strings
           
          



