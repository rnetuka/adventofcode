import math
from lib.matrix import Matrix

top_connections = ['|', 'F', '7']
bottom_connections = ['|', 'L', 'J']
left_connections = ['-', 'F', 'L']
right_connections = ['-', 'J', '7']


class PipeMaze:

    def __init__(self):
        self.tiles = None
        self.start = None

    @staticmethod
    def from_file(path):
        lines = []
        with open(path) as file:
            for line in file.readlines():
                lines.append(line.rstrip())
        width = len(lines[0])
        height = len(lines)
        maze = PipeMaze()
        maze.tiles = Matrix(rows=height, columns=width)
        for i in range(height):
            for j in range(width):
                tile = lines[i][j]
                maze.tiles[i][j] = tile
                if tile == 'S':
                    maze.start = (i, j)
        return maze

    def tile(self, coordinates):
        return self.tiles.peek(*coordinates) and self.tiles[coordinates[0]][coordinates[1]]

    def append_top_if_connects(self, top, neighbors):
        if self.tiles.peek(*top) in top_connections:
            neighbors.append(top)

    def append_bottom_if_connects(self, bottom, neighbors):
        if self.tiles.peek(*bottom) in bottom_connections:
            neighbors.append(bottom)

    def append_left_if_connects(self, left, neighbors):
        if self.tiles.peek(*left) in left_connections:
            neighbors.append(left)

    def append_right_if_connects(self, right, neighbors):
        if self.tiles.peek(*right) in right_connections:
            neighbors.append(right)

    def neighbors_of(self, i, j):
        pipe = self.tiles[i][j]
        top = (i - 1, j)
        bottom = (i + 1, j)
        left = (i, j - 1)
        right = (i, j + 1)

        neighbors = []
        if pipe == 'S':
            self.append_top_if_connects(top, neighbors)
            self.append_bottom_if_connects(bottom, neighbors)
            self.append_left_if_connects(left, neighbors)
            self.append_right_if_connects(right, neighbors)

        if pipe == '|':
            self.append_top_if_connects(top, neighbors)
            self.append_bottom_if_connects(bottom, neighbors)

        if pipe == '-':
            self.append_left_if_connects(left, neighbors)
            self.append_right_if_connects(right, neighbors)

        if pipe == 'L':
            self.append_top_if_connects(top, neighbors)
            self.append_right_if_connects(right, neighbors)

        if pipe == 'J':
            self.append_top_if_connects(top, neighbors)
            self.append_left_if_connects(left, neighbors)

        if pipe == '7':
            self.append_left_if_connects(left, neighbors)
            self.append_bottom_if_connects(bottom, neighbors)

        if pipe == 'F':
            self.append_right_if_connects(right, neighbors)
            self.append_bottom_if_connects(bottom, neighbors)

        return neighbors


def get_loop():
    maze = PipeMaze.from_file('input/day10.txt')
    loop = set()
    queue = [maze.start]
    while len(queue) > 0:
        node = queue.pop(0)
        for neighbor in maze.neighbors_of(*node):
            if neighbor not in loop:
                loop.add(neighbor)
                queue.append(neighbor)
    return loop


def solution_1():
    loop = get_loop()
    return math.ceil(len(loop) / 2)


def solution_2():
    maze = PipeMaze.from_file('input/day10.txt')
    loop = get_loop()

    inside_tiles = 0
    for i, j in maze.tiles.coordinates:
        if (i, j) not in loop:
            # for each tile not in the loop itself, check in how many tiles does a vector (+x, +y) intersect the loop
            # if there is an odd number of intersections, the tile must be located inside the loop polygon
            i2, j2 = i, j
            intersections = 0
            while i2 < maze.tiles.height and j2 < maze.tiles.width:
                content = maze.tiles[i2][j2]
                # exclude intersections with edges since the vector leads between the edge and the other tile in such
                # case
                if (i2, j2) in loop and content not in ['L', '7']:
                    intersections += 1

                i2 += 1
                j2 += 1

            if intersections % 2 == 1:
                inside_tiles += 1

    return inside_tiles


if __name__ == '__main__':
    print('--- Day 10: Pipe Maze ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
