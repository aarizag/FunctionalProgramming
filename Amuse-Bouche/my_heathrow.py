from typing import List, Tuple
from functools import reduce
from time import time


class Road:
    """
    Object representation of a Road with values to denote it's length and position on the map
    """

    # road_id = 0

    def __init__(self, distance: int, pos: str = ""):
        self.distance = distance
        self.position = pos
        # self.id = Road.road_id
        # Road.road_id += 1

    def __str__(self):
        return f"Pos: {self.position}  |  Dist: {self.distance}"


class Path:
    """
    Object representation of a series of roads and the distance to travel those roads
    """

    def __init__(self, dist: int = 0, roads: List[Road] = None, start: str = None):
        self.roads = [] if roads is None else roads
        self.dist = dist
        self.start = start

    def __lt__(self, other):
        """
        Define the "less than" function for Path:
            A Path is considered less than another Path if the distance is less than the other
            If they are the same, it is considered less if the number of roads in it is less than the other

        :param other: the Path it is being compared to
        :return: Boolean
        """
        return (self.dist, len(self.roads)) < (other.dist, len(other.roads))

    def __add__(self, other):
        """
        Define addition for Paths

        :param other: the Path it is being added
        :return: A new Path with the combined distances and combined road lists as parameters
        """
        return Path(self.dist + other.dist, self.roads + other.roads, start=self.start)


def all_paths(a: int, b: int, c: int) -> (Path, Path, Path, Path):
    """
    :param a, b, c: Integers denoting the "distance" of the road
    :return: Four Paths representing both possible routes to A (top) and B (bottom)
             written as follows: (Path to A from A, Path to B from A, Path to A from B, Path to B from B)
    """
    road_a = Road(a, "A")
    road_b = Road(b, "B")
    road_c = Road(c, "C")
    return (Path(a, [road_a], start="A"),
            Path(a + c, [road_a, road_c], start="A"),
            Path(b + c, [road_b, road_c], start="B"),
            Path(b, [road_b], start="B"))


def find_best(r_vals) -> (Path, Path):
    """
    :param r_vals: A tuple containing 3 values for roads (A,B,C respectively)
    :return: A tuple containing the  (Optimum path to A, Optimum Path to B)
    """
    (a_a, b_a, a_b, b_b) = all_paths(*r_vals)
    return a_a if a_a < a_b else a_b, \
           b_a if b_a < b_b else b_b


def combine_paths(old_a: Path, old_b: Path, a: Path, b: Path) -> (Path, Path):
    """
    :param old_a, old_b: The previous best paths to A and B, respectively
    :param a, b: The local best paths to A and B in the current set of four possible paths
    :return: A tuple containing the best local paths to A and B respectively combined with the best Path ending at the
             best local paths' starting points
             e.g. if the best local path to A starts at B, combine it with the old best path to B
    """
    best_a = old_a + a if a.start == "A" else old_b + a
    best_b = old_b + b if b.start == "B" else old_a + b
    return best_a, best_b


def current_optimum(best: Tuple[Path, Path], r_vals: Tuple[int, int, int]) -> (Path, Path):
    """
    :param best: A tuple containing the (previous best path to A, previous best path to B)
    :param r_vals: A tuple containing 3 values for roads (A,B,C respectively)
    :return: A tuple containing the best path from start to current to A and B, respectively
    """
    return combine_paths(*best, *find_best(r_vals))
    # (old_a, old_b) = best
    # (new_a, new_b) = find_best(*r_vals)
    # return combine_paths(old_a, old_b, new_a, new_b)


def optimal_path(inp: [int]) -> Path:
    """
    :param inp: A list of numbers that is represents the distance of Roads in a series of intersections
                Input is given in 3s, visualized as:
                [(top road, bottom road, vertical right road connecting the other two) ...]
    :return: The fastest path traversing the series of intersections
    """
    inp += [0] * (len(inp) % 3)  # If len(inp)%3 != 0, adds segments of length 0.
    roads = zip(inp[::3], inp[1::3], inp[2::3])  # split the input into a series of tuples with 3 elements each
    accumulator = (Path(start="A"), Path(start="B"))  # empty paths to start the accumulator

    (a, b) = reduce(current_optimum, roads, accumulator)
    return a if a < b else b


def print_path(p: Path, test_num: int = 0) -> None:
    """
    :param p: Path to be printed
    :param test_num: The current test number
    :return: None
    """
    print(f"\n\nTest {test_num} results in a Path starting at {p.start} and ending at {p.roads[-1].position}\nRoads: ")
    for r in p.roads:
        print(r)


test_input = [50, 10, 30, 5, 90, 20, 40, 2, 25, 10, 8, 0]
test_input2 = [15, 5, 10, 10, 30, 10, 5, 20, 5, 35, 15, 20, 15, 10, 0]

# st = time()
op = optimal_path(test_input)
# print("time=", time() - st)
print_path(op, test_num=1)
Road.road_id = 0
print_path(optimal_path(test_input2), test_num=2)
