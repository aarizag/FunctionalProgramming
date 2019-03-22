from functools import reduce, wraps
from typing import Any, Callable, Dict, List, Tuple, TypeVar
from time import time


class MetaRoad(type):
    """
    This class allows us to define __str__ on Classes. It also lets us define opposite on classes.
    """

    def __str__(cls):
        return cls.__name__

    # An empty dictionary. Keys and values are Road Classes, i.e., of type MetaRoad.
    # Would like to write: {A: B, B: A}, but can't use A or B before they are declared.
    # Must quote MetaRoad in the type-annotation because it is not yet (fully) defined.
    oppositeRoadDict: Dict['MetaRoad', 'MetaRoad'] = {}

    def opposite(cls):
        return MetaRoad.oppositeRoadDict[cls]


class Road(metaclass=MetaRoad):

    def __init__(self, dist: int):
        self.dist = dist

    def __str__(self):
        """
        This defines the string representation of a segment, i.e., A(5).
        The format is the same as in the Haskell code.
        """
        return f'{type(self).__name__}/{self.dist}'


class A(Road):

    def __init__(self, dist: int):
        # Can't do this in MetaRoad. Will get names A and B are undefined.
        if not A in MetaRoad.oppositeRoadDict:
            MetaRoad.oppositeRoadDict[A] = B
        super().__init__(dist)


class B(Road):

    def __init__(self, dist: int):
        # Can't do this in MetaRoad. Will get names A and B are undefined.
        if not B in MetaRoad.oppositeRoadDict:
            MetaRoad.oppositeRoadDict[B] = A
        super().__init__(dist)


class C(Road):
    ...  # This is like pass


class Path:

    def __init__(self, steps: List[Road]):
        self.steps = steps

    def __add__(self, otherPath: 'Path') -> 'Path':
        return Path(self.steps + otherPath.steps)

    def __str__(self) -> str:
        st = f'{self.startRoad().__name__}->{self.endRoad().__name__}. Dist: {self.dist()}. ' + \
             listToString(self.steps, start='', end='')
        return st

    def dist(self) -> int:
        return sum((step.dist for step in self.steps))

    def endRoad(self) -> MetaRoad:
        """
        Returns a Road, which is of type MetaRoad.

        If the final Path segment is a C, use the penultimate segment.
        :return: The class, i.e., the Road, where the Path ends.
        """
        rd = type(self.steps[-1])
        # Calls opposite() in MetaRoad, which is where the methods for Road classes as objects are defined.
        return rd if rd != C else type(self.steps[-2]).opposite()

    def startRoad(self) -> MetaRoad:
        """
        Returns a Road, which is of type MetaRoad.

        :return: The class, i.e., the Road, where the Path starts.
        """
        return type(self.steps[0])


class QuadPaths:
    """
    The shortest Paths from A and B to A and B in all combinations.
    """

    def __init__(self, paths: List[Path]):
        self.paths = paths

    def __str__(self) -> str:
        st = listToString(self.paths, start='QuadPaths:\n    ', sep='\n    ', end='')
        return (st)


T2 = TypeVar('T2')


def trace(func: Callable[..., T2]) -> Callable[..., T2]:
    """
    Print the function signature and return value.
    Adapted from the @debug decorator of Hjelle, Primer on Python Decorators
    (https://realpython.com/primer-on-python-decorators/#debugging-code)
    """

    @wraps(func)
    def wrapper_trace(*args: List[Any], **kwargs: List[Any]) -> T2:
        args_str = [str(a) for a in args]
        kwargs_str = [f'{k}={str(v)}' for (k, v) in kwargs.items()]
        fullArgsStr = listToString(args_str + kwargs_str, start='\n', sep=',\n', end='\n')
        print(f'\nCalling {func.__name__}({fullArgsStr})')
        value = func(*args, **kwargs)
        valueStr = str(value) if type(value) is not list else listToString(value, start='', sep=',\n', end='\n')
        print(f'{func.__name__} returned: \n{valueStr}\n')
        return value

    return wrapper_trace


def bestPath(start: Road, qp1: QuadPaths, qp2: QuadPaths, end: Road) -> Path:
    """
    Find the best pair of Paths from qp1 and qp2 such that:
    the qp1 Path starts at Road start;
    the qp2 Path starts where the qp1 Path ends;
    the qp2 Path ends at Road end.
    Join those two Paths into a single combined Path and return that combined Path.

    Note: (+) is defined for Paths to join two Paths into a new Path.
    See Path.__add__().
    """
    paths = [p1 + p2 for p1 in qp1.paths if p1.startRoad() == start
             for p2 in qp2.paths if p1.endRoad() == p2.startRoad() and p2.endRoad() == end]
    sortd = sorted(paths, key=dist_numsteps)
    return sortd[0]


def dist_numsteps(p: Path) -> Tuple[int, int]:
    """
    When comparing two paths, the one with the sorter distance is better.
    If they have the same distance, the one with the fewer steps is better.
    This function returns a value that can be compared to values from other Paths.
    """
    return (p.dist(), len(p.steps))


@trace
def joinQuadPaths(qp1: QuadPaths, qp2: QuadPaths) -> QuadPaths:
    joinedQuadPaths = QuadPaths([bestPath(s, qp1, qp2, e) for s in [A, B] for e in [A, B]])
    return joinedQuadPaths


T1 = TypeVar('T1')


def listToString(aList: List[T1], start='[', sep=', ', end=']') -> str:
    return start + sep.join([str(elt) for elt in aList]) + end


def optimalPath(allSegs: List[int]) -> Path:
    """
    Returns a Path with the shortest dist from Heathrow to London.
    """
    qpList = toQPList(allSegs)
    finalPaths = reduce(joinQuadPaths, qpList).paths
    return min(finalPaths, key=dist_numsteps)


def segsToQP(aDist: int, bDist: int = 0, cDist: int = 0) -> QuadPaths:
    return QuadPaths([Path([A(aDist)]),  # A -> A
                      Path([A(aDist), C(cDist)]),  # A -> B
                      Path([B(bDist), C(cDist)]),  # B -> A
                      Path([B(bDist)])  # B -> B
                      ])


@trace
def toQPList(allSegs: List[int]) -> List[QuadPaths]:
    """
    If len(allSegs)%3 != 0, assumes additional segments of length 0.

    Doing it iteratively rather than recursively so that @trace will be called only once.
    """
    qpList: List[QuadPaths] = []
    while len(allSegs) > 0:
        # Uses qpList and allSegs mutably
        qpList.append(segsToQP(*allSegs[:3]))
        allSegs = allSegs[3:]
    return qpList


if __name__ == '__main__':
    # The example from the book.
    dists = [50, 10, 30, 5, 90, 20, 40, 2, 25, 10, 8]
    # st = time()
    op = optimalPath(dists)
    # print("time = ", time() - st, op)
    print(op)
    # => B->B. Dist: 75. [B/10, C/30, A/5, C/20, B/2, B/8],
