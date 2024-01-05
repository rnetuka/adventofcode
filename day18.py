from lib.scanner import tokenize
from shapely import geometry


dx = {'U': +0, 'D': +0, 'L': -1, 'R': +1}
dy = {'U': -1, 'D': +1, 'L': +0, 'R': +0}
direction_codes = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}


def create_polygon(instructions):
    x = 0
    y = 0
    points = []
    for direction, distance, _ in instructions:
        points.append((x, y))
        x += distance * dx[direction]
        y += distance * dy[direction]

    return geometry.Polygon(points)


def points_in_polygon(polygon):
    # in a rectangle (0, 0), (5, 0), (5, 2), (0, 2) the area is 5 * 2 = 10 units
    # length of the boundary line is 5+2+5+2 = 14 units
    # however, there are only 4 points inside the rectangle plus additional 14 points on the boundary line
    # (= 18 points in total)
    return int(polygon.area + polygon.length / 2 + 1)


def solution_1():
    with open('input/day18.txt') as file:
        instructions = [tokenize(line, types=(str, int, str)) for line in file.readlines()]
        polygon = create_polygon(instructions)
        return points_in_polygon(polygon)


def solution_2():
    with open('input/day18.txt') as file:
        instructions = [tokenize(line, types=(str, int, str)) for line in file.readlines()]
        for i in range(len(instructions)):
            _, _, color = instructions[i]
            direction = direction_codes[color[-2:-1]]
            distance = int(color[2:-2], 16)
            instructions[i] = (direction, distance, color)
        polygon = create_polygon(instructions)
        return points_in_polygon(polygon)


if __name__ == '__main__':
    print('--- Day 18: Lavaduct Lagoon ---')
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
