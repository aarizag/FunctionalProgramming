# parse_name.py


import parse

"""
Function : parse_name
@param : text, a string
"""
def parse_name(text: str) -> str:

    # Tuple of strings with likely formats for declaring a name
    # effectively used as a regular expression
    patterns = (

        "my name is {name}",

        "i'm {name}",

        "i am {name}",

        "call me {name}",

        "{name}",

    )

    for pattern in patterns:

        # If the text inputted by the user matches a pattern by comparing the
        # text with the patterns
        result = parse.parse(pattern, text)

        # If the result is not None
        # IOW, if the text matched one of the expressions
        if result:

            return result["name"]

    return ""


answer = input("What is your name? ")

name = parse_name(answer)

print(f"Hi {name}, nice to meet you!")