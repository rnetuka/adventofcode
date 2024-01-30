from lib.interval import Interval


class Brick:

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def parse(string):
        left, right = string.split('~')
        x1, y1, z1 = [int(n) for n in left.split(',')]
        x2, y2, z2 = [int(n) for n in right.split(',')]
        brick = Brick()
        brick.x = Interval(x1, x2)
        brick.y = Interval(y1, y2)
        brick.z = Interval(z1, z2)
        return brick

    def intersects_with(self, other):
        return self.x.intersect(other.x) and self.y.intersect(other.y)


class Game:

    def __init__(self, levels=1):
        self.bricks = []
        self.floors = {}
        for z in range(levels):
            self.floors[z] = set()
        self.supports = {}
        self.supported_by = {}

    def add_brick(self, brick):
        self.bricks.append(brick)
        self.supports[brick] = set()
        self.supported_by[brick] = set()
        for z in brick.z:
            self.floors[z].add(brick)

    def is_empty(self, xi, yi, z):
        if z == 0:
            return False
        else:
            return not any(xi.intersect(brick.x) and yi.intersect(brick.y) for brick in self.floors[z])

    def run(self):
        self.bricks.sort(key=lambda brick: brick.z.start)

        for brick in self.bricks:
            while self.is_empty(brick.x, brick.y, brick.z.start - 1):
                self.floors[brick.z.end].remove(brick)
                brick.z.end -= 1
                brick.z.start -= 1
                self.floors[brick.z.start].add(brick)

        # calculate what bricks support others
        for brick in self.bricks:
            self.supported_by[brick].update(self.supporting_bricks(brick))
            self.supports[brick].update(self.brick_supports(brick))

    def disintegrate(self, brick):
        chain = []

        supported_by = {}
        for b in self.supported_by:
            supported_by[b] = set(self.supported_by[b])

        for other in self.bricks_above(brick):
            if supported_by[other] == {brick}:
                chain.append(other)

        total_falling = set()

        while len(chain) > 0:
            falling = chain.pop(0)
            total_falling.add(falling)

            for other in [o for o in self.bricks_above(falling) if o != falling and o not in chain]:
                if falling in supported_by[other]:
                    supported_by[other].remove(falling)
                    if len(supported_by[other]) == 0:
                        chain.append(other)

        return total_falling

    def bricks_above(self, brick):
        z = brick.z.end
        return self.floors[z + 1]

    def bricks_below(self, brick):
        z = brick.z.start
        return self.floors[z - 1]

    def supporting_bricks(self, brick):
        return set(bottom for bottom in self.bricks_below(brick) if brick.intersects_with(bottom))

    def brick_supports(self, brick):
        return set(top for top in self.bricks_above(brick) if brick.intersects_with(top))


def read_input():
    bricks = []
    with open('input/day22.txt') as file:
        for line in file.readlines():
            bricks.append(Brick.parse(line))

    levels = max(brick.z.end for brick in bricks)

    game = Game(levels + 1)
    for brick in bricks:
        game.add_brick(brick)

    return game


def safe_to_disintegrate_bricks(game):
    safe_to_disintegrate = set()

    for brick in game.bricks:
        supported = game.supports[brick]
        if all(len(game.supported_by[s]) > 1 for s in supported):
            safe_to_disintegrate.add(brick)

    return safe_to_disintegrate


def solution_1():
    game = read_input()
    game.run()
    return len(safe_to_disintegrate_bricks(game))


def solution_2():
    game = read_input()
    game.run()
    all_bricks = set(game.bricks)
    safe_to_disintegrate = safe_to_disintegrate_bricks(game)
    unsafe_to_disintegrate = all_bricks.difference(safe_to_disintegrate)

    n = 0
    for brick in unsafe_to_disintegrate:
        falling = game.disintegrate(brick)
        n += len(falling)

    return n


if __name__ == '__main__':
    print('--- Day 22: Sand Slabs ---')
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
