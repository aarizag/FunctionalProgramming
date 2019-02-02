# do_twice.py


from typing import Callable


"""
Function : do_twice
purpose : perform a callable function with a single argument twice
@:param
    func (a callable function that takes a string as an argument and returns a string)
    argument (string)
"""
def do_twice(func: Callable[[str], str], argument: str) -> None:

    print(func(argument))

    print(func(argument))


def create_greeting(name: str) -> str:
    # return the string "Hello" + the name parameter
    return f"Hello {name}"


do_twice(create_greeting, "Jekyll")

# >>> Hello Jekyll
# >>> Hello Jekyll
