class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f'({self.x}, {self.y})'


def manhattan_distance(a, b):
    if isinstance(a, Point) and isinstance(b, Point):
        return abs(a.x - b.x) + abs(a.y - b.y)

    if isinstance(a, tuple) and len(a) == 2 and isinstance(b, tuple) and len(b) == 2:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
