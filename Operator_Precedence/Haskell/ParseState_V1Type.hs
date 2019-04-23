module ParseState_V1Type (ParseState_V1) where

import DataDeclrs (Elmt) 
import ParseStateClass (ParseState(..)) 


---------------------------------------------------------------------
-- Define  ParseState_V1  to be an [Elmt] list with an index
-- indicating the start of the window.   
---------------------------------------------------------------------
 
data ParseState_V1 = IndexAndList Int [Elmt] deriving Eq


-- Define how to perform the ParseState functions on ParseState_V1 objects
instance ParseState ParseState_V1 where

  initialParseState tokens = IndexAndList 0 tokens

  fromListPair (left, right) = 
    IndexAndList (length left) (reverse left ++ right)

  toListPair (IndexAndList n list) = revfirst $ splitAt n list
    where revfirst (revLeft, right) = (reverse revLeft, right)
 