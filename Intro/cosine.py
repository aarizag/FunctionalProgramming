# cosine.py


import numpy as np

"""
Function : print_cosine
purpose : print the cosine of the array into the console
@:param
    x (an n-dimensional array from numpy)
"""
def print_cosine(x: np.ndarray) -> None:

    with np.printoptions(precision=3, suppress=True):

        print(np.cos(x))


x = np.linspace(0, 2 * np.pi, 9)

print_cosine(x)