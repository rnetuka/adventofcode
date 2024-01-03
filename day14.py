from lib.matrix import Matrix


def tilt_north(column):
    tilted = True
    while tilted:
        tilted = False
        for i in range(1, len(column)):
            if column[i] == 'O' and column[i - 1] == '.':
                column[i] = '.'
                column[i - 1] = 'O'
                tilted = True


def tilt_south(column):
    tilted = True
    while tilted:
        tilted = False
        for i in range(len(column) - 1):
            if column[i] == 'O' and column[i + 1] == '.':
                column[i] = '.'
                column[i + 1] = 'O'
                tilted = True


def tilt_east(row):
    tilted = True
    while tilted:
        tilted = False
        for j in range(len(row) - 1):
            if row[j] == 'O' and row[j + 1] == '.':
                row[j] = '.'
                row[j + 1] = 'O'
                tilted = True


def tilt_west(row):
    tilted = True
    while tilted:
        tilted = False
        for j in range(1, len(row)):
            if row[j] == 'O' and row[j - 1] == '.':
                row[j] = '.'
                row[j - 1] = 'O'
                tilted = True


def total_load(matrix):
    n = 0
    for i, j in matrix.coordinates:
        if matrix[i][j] == 'O':
            n += matrix.height - i
    return n


def read_input():
    return Matrix.from_file('input/day15.txt')


def solution_1():
    matrix = read_input()
    for j in range(matrix.width):
        column = matrix.columns[j]
        tilt_north(column)
    n = 0
    for i, j in matrix.coordinates:
        if matrix[i][j] == 'O':
            n += matrix.height - i
    return n


def solution_2():
    matrix = read_input()
    history = set()
    history_map = {}
    cycle = 0
    while True:
        for j in range(matrix.width):
            column = matrix.columns[j]
            tilt_north(column)
        for i in range(matrix.height):
            row = matrix.rows[i]
            tilt_west(row)
        for j in range(matrix.width):
            column = matrix.columns[j]
            tilt_south(column)
        for i in range(matrix.height):
            row = matrix.rows[i]
            tilt_east(row)

        cycle += 1

        if repr(matrix) in history:
            cycle = 1_000_000_000 - (1_000_000_000 - cycle) % (cycle - history_map[repr(matrix)])

        history.add(repr(matrix))
        history_map[repr(matrix)] = cycle

        if cycle >= 1_000_000_000:
            break
    n = 0
    for i, j in matrix.coordinates:
        if matrix[i][j] == 'O':
            n += matrix.height - i
    return n


if __name__ == '__main__':
    print('--- Day 14: Parabolic Reflector Dish ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
