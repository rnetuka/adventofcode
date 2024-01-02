import itertools
from lib.matrix import Matrix
from lib.metrics import Point, manhattan_distance


def is_empty(row):
    return all(element == '.' for element in row)


def sum_distances(insert_count):
    matrix = Matrix.from_file('input/day11.txt')
    points = [Point(i, j) for i, j in matrix.coordinates if matrix[i][j] == '#']
    already_calculated = set()

    # rows as a list of True/False value reflecting whether the row is empty or not
    rows = [is_empty(matrix.row(i)) for i in range(matrix.height)]

    # columns as a list of True/False value reflecting whether the column is empty or not
    columns = [is_empty(matrix.column(j)) for j in range(matrix.width)]

    d = 0
    for p1, p2 in itertools.product(points, points):
        if p1 != p2:
            if (p2, p1) in already_calculated:
                continue

            min_i = min(p1.x, p2.x)
            max_i = max(p1.x, p2.x)
            row_range = rows[min_i:max_i]
            empty_rows = sum(1 if row else 0 for row in row_range)

            min_j = min(p1.y, p2.y)
            max_j = max(p1.y, p2.y)
            column_range = columns[min_j:max_j]
            empty_columns = sum(1 if column else 0 for column in column_range)

            distance = manhattan_distance(p1, p2)
            distance += empty_rows * insert_count
            distance += empty_columns * insert_count
            d += distance

            already_calculated.add((p1, p2))
    return d


def solution_1():
    return sum_distances(insert_count=1)


def solution_2():
    return sum_distances(insert_count=1_000_000 - 1)


if __name__ == '__main__':
    print('--- Day 11: Cosmic Expansion ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
