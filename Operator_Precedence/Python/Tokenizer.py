from Operator_Precedence.Python.DataDeclrs import *

def add_spaces(s: str) -> str:
        return " ".join(s.replace(" ", ""))


"""
-- What does makeToken assume about the input String? 
-- The symbol for division is '/', but the operation performed is `div`.
-- How can you tell that from this table? 
makeToken :: String -> Elmt
makeToken str = 
  case M.lookup str $
           fromList [ ( "(", LPar), ( ")", RPar) 
                    , ( "+", Op (+) '+' 1 'L'), ( "-", Op (-) '-' 1 'L') 
                    , ( "*", Op (*) '*' 2 'L'), ( "/", Op div '/' 2 'L') 
                    , ( "^", Op (^) '^' 3 'R')
                    ] of
  Just op -> op
  Nothing -> Nbr (read str) -- How do we know we should perform: read str? 
                            -- How do we know what type  read  returns? 
"""

def make_token(s: str) -> Elmt:
    pass
