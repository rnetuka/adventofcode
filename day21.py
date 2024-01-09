from lib.matrix import Matrix


class Map:

    def __init__(self):
        self.tiles = Matrix.from_file('input/day21.txt')
        for i, j in self.tiles.coordinates:
            if self.tiles[i][j] == 'S':
                self.start = (i, j)

    def neighbors_of(self, tile):
        i, j = tile
        neighbors = []
        for other_i, other_j in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
            if self.tiles.peek(other_i, other_j) in ['.', 'S']:
                neighbors.append((other_i, other_j))
        return neighbors


def solution_1():
    map = Map()
    tiles = {map.start}
    for step in range(64):
        next = set()
        for tile in tiles:
            for neighbor in map.neighbors_of(tile):
                next.add(neighbor)
        tiles = next
    return len(tiles)


if __name__ == '__main__':
    print('--- Day 21: Step Counter ---')
    print(f'Part 1: {solution_1()}')
