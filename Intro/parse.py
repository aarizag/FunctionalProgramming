# parse.pyi
# This is the equivalent of a java interface or a C++ header
# There are classes and methods defined, but no actual code for using them.

from typing import Any, Mapping, Optional, Sequence, Tuple, Union

"""
Class: Result
@params_for_init : 
    fixed (Sequence of strings, e.g. list, tuple) 
    named (Mapping of strings to strings, e.g. dictionary)
    spans (Mapping of int to a Tuple of 2 ints) 
"""
class Result:
    def __init__(
        self,
        fixed: Sequence[str],
        named: Mapping[str, str],
        spans: Mapping[int, Tuple[int, int]],
    ) -> None: ...
    def __getitem__(self, item: Union[int, str]) -> str: ...
    def __repr__(self) -> str: ...


"""
Function: parse
@:param
    format (string)
    string (string),
    evaluate_result (boolean): this is a keyword parameter
    case_sensitive (boolean): this is a keyword parameter
@:return
    Will either return an object of type Result or None
"""
def parse(
    format: str,
    string: str,
    evaluate_result: bool = ...,
    case_sensitive: bool = ...,
) -> Optional[Result]: ...