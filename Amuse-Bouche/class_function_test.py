class Road(type):
    def __str__(cls):
        return cls.__name__


class Segment(metaclass=Road):
    def __init__(self, dist: int):
        self.dist = dist

    def __str__(self):
        return str(type(self))# f'{str(type(self))}/{self.dist}'


class A(Segment):
    """
    Segments of the A road.
    """


class B(Segment):
    """ Segments of the B road. """


class C(Segment):
    """ Segments of the C road. """

