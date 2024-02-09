from lib.matrix import Matrix


class Maze:

    def __init__(self):
        self.tiles = Matrix.from_file('input/day23.txt')

    @property
    def start(self):
        return 0, 1

    @property
    def finish(self):
        return self.tiles.height - 1, self.tiles.width - 2

    def is_crossroad(self, tile):
        i, j = tile[0], tile[1]
        top = (i - 1, j)
        bottom = (i + 1, j)
        left = (i, j - 1)
        right = (i, j + 1)

        neighbors = []
        if self.tiles.peek(top) in ['.', '^', 'v']:
            neighbors.append(top)
        if self.tiles.peek(bottom) in ['.', 'v', '^']:
            neighbors.append(bottom)
        if self.tiles.peek(left) in ['.', '<', '>']:
            neighbors.append(left)
        if self.tiles.peek(right) in ['.', '>', '>']:
            neighbors.append(right)

        return len(neighbors) >= 3

    def is_move_up_possible(self, current):
        i, j = current[0], current[1]
        next_content = self.tiles.peek(i - 1, j)
        return next_content in ['.', '^']

    def is_move_down_possible(self, current):
        i, j = current[0], current[1]
        next_content = self.tiles.peek(i + 1, j)
        return next_content in ['.', 'v']

    def is_move_left_possible(self, current):
        i, j = current[0], current[1]
        next_content = self.tiles.peek(i, j - 1)
        return next_content in ['.', '<']

    def is_move_right_possible(self, current):
        i, j = current[0], current[1]
        next_content = self.tiles.peek(i, j + 1)
        return next_content in ['.', '>']

    def next_move_tiles(self, previous, current):
        i, j = current[0], current[1]
        neighbors = set()

        if self.is_move_up_possible(current):
            neighbors.add((i - 1, j))

        if self.is_move_down_possible(current):
            neighbors.add((i + 1, j))

        if self.is_move_left_possible(current):
            neighbors.add((i, j - 1))

        if self.is_move_right_possible(current):
            neighbors.add((i, j + 1))

        return neighbors - previous

    def proceed(self, previous, current, distance):
        while current != self.finish:
            if self.is_crossroad(current):
                next_tiles = self.next_move_tiles(previous, current)
                if len(next_tiles) == 0:
                    return 0
                return max(self.proceed(previous=previous.union({current}), current=next, distance=distance+1) for next in next_tiles)
            else:
                next_tiles = self.next_move_tiles(previous, current)
                if len(next_tiles) == 1:
                    previous.add(current)
                    current = list(next_tiles)[0]
                    distance += 1
                else:
                    return 0

        return distance

    def longest_path(self):
        return self.proceed(previous=set(), current=self.start, distance=0)


def solution_1():
    maze = Maze()
    return maze.longest_path()


if __name__ == '__main__':
    print('--- Day 23: A Long Walk ---')
    print(f'Part 1: {solution_1()}')
