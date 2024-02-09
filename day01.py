from collections import namedtuple
from lib.circular_buffer import CircularBuffer
from lib.metrics import manhattan_distance


Vector = namedtuple('Vector', ['dx', 'dy'])
North = Vector(dx=0, dy=-1)
East = Vector(dx=1, dy=0)
South = Vector(dx=0, dy=1)
West = Vector(dx=-1, dy=0)


class Walk:

    def __init__(self):
        self.directions = CircularBuffer([North, East, South, West])
        self.x = 0
        self.y = 0
        self.facing = North
        self.visited = set()
        self.found = None

    def process(self, instruction):
        direction = instruction[0]
        distance = int(instruction[1:])
        self.turn(direction)
        return self.move(distance)

    def turn(self, direction):
        if direction == 'L':
            i = self.directions.index(self.facing) - 1
            self.facing = self.directions[i]
        elif direction == 'R':
            i = self.directions.index(self.facing) + 1
            self.facing = self.directions[i]

    def move(self, distance):
        for _ in range(distance):
            self.x += self.facing.dx
            self.y += self.facing.dy
            if not self.found and (self.x, self.y) in self.visited:
                self.found = (self.x, self.y)
            self.visited.add((self.x, self.y))

    def follow(self, instructions):
        for instruction in instructions:
            self.process(instruction)
        return manhattan_distance((0, 0), (self.x, self.y))

    def search_for(self, instructions):
        for instruction in instructions:
            self.process(instruction)
        return manhattan_distance((0, 0), self.found)


def read_instructions():
    with open('input/day01.txt') as file:
        return file.read().rstrip().split(', ')


def solution_1():
    walk = Walk()
    return walk.follow(read_instructions())


def solution_2():
    walk = Walk()
    return walk.search_for(read_instructions())


if __name__ == '__main__':
    print('--- Day 1: No Time for a Taxicab ---')
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
