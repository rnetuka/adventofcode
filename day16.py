from concurrent.futures import ProcessPoolExecutor
from lib.matrix import Matrix


class Beam:

    def __init__(self, i=0, j=0, facing='right'):
        self.i = i
        self.j = j
        self.facing = facing


class Contraptions:

    def __init__(self):
        self.maze = Matrix.from_file('input/day16.txt')
        self.beams = []
        self.energized = set()
        self.visited = set()

    def place_beam(self, beam):
        self.beams.append(beam)
        self.energized.add((beam.i, beam.j))
        self.visited.add((beam.i, beam.j, beam.facing))

    def tick(self):
        for beam in self.beams:
            di = 0
            dj = 0
            if beam.facing == 'top':
                di = -1
            elif beam.facing == 'right':
                dj = 1
            elif beam.facing == 'bottom':
                di = 1
            elif beam.facing == 'left':
                dj = -1
            next_i = beam.i + di
            next_j = beam.j + dj
            if next_i < 0 or next_i >= self.maze.height:
                beam.facing = None
                continue
            if next_j < 0 or next_j >= self.maze.width:
                beam.facing = None
                continue
            beam.i = next_i
            beam.j = next_j
            tile = self.maze[beam.i][beam.j]
            if (beam.i, beam.j, beam.facing) in self.visited:
                beam.facing = None
                continue
            self.visited.add((beam.i, beam.j, beam.facing))
            self.energized.add((beam.i, beam.j))
            if tile == '/':
                if beam.facing == 'top':
                    beam.facing = 'right'
                elif beam.facing == 'right':
                    beam.facing = 'top'
                elif beam.facing == 'bottom':
                    beam.facing = 'left'
                elif beam.facing == 'left':
                    beam.facing = 'bottom'
            elif tile == '\\':
                if beam.facing == 'top':
                    beam.facing = 'left'
                elif beam.facing == 'right':
                    beam.facing = 'bottom'
                elif beam.facing == 'bottom':
                    beam.facing = 'right'
                elif beam.facing == 'left':
                    beam.facing = 'top'
            elif tile == '|':
                if beam.facing in ['left', 'right']:
                    beam.facing = 'top'
                    self.beams.append(Beam(beam.i, beam.j, facing='bottom'))
            elif tile == '-':
                if beam.facing in ['top', 'bottom']:
                    beam.facing = 'left'
                    self.beams.append(Beam(beam.i, beam.j, facing='right'))
        self.beams = [beam for beam in self.beams if beam.facing is not None]

    def run(self):
        while any(beam.facing is not None for beam in self.beams):
            self.tick()
        return len(self.energized)


def solution_1():
    contraptions = Contraptions()
    contraptions.place_beam(Beam())
    contraptions.run()
    return len(contraptions.energized)


def solution_2():
    contraptions = Contraptions()
    height = contraptions.maze.height
    width = contraptions.maze.width
    mazes = []
    for i in range(height):
        maze = Contraptions()
        maze.place_beam(Beam(i, j=0, facing='right'))
        mazes.append(maze)
    for i in range(height):
        maze = Contraptions()
        maze.place_beam(Beam(i, j=width-1, facing='left'))
        mazes.append(maze)
    for j in range(width):
        maze = Contraptions()
        maze.place_beam(Beam(i=0, j=j, facing='bottom'))
        mazes.append(maze)
    for j in range(width):
        maze = Contraptions()
        maze.place_beam(Beam(i=height-1, j=j, facing='top'))
        mazes.append(maze)

    with ProcessPoolExecutor() as executor:
        return max(executor.map(Contraptions.run, mazes))


if __name__ == '__main__':
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
