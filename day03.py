from lib.matrix import Matrix


def read_input():
    return Matrix.from_file('input/day03.txt')


class NumberBuilder:

    def __init__(self):
        self.number = ''
        self.number_coordinates = []

    def append(self, digit, coordinates):
        self.number += digit
        self.number_coordinates.append(coordinates)


def neighbor_coordinates(list):
    result = set()
    for i, j in list:
        result.add((i - 1, j - 1))
        result.add((i - 1, j))
        result.add((i - 1, j + 1))
        result.add((i, j - 1))
        result.add((i, j + 1))
        result.add((i + 1, j - 1))
        result.add((i + 1, j))
        result.add((i + 1, j + 1))
    return result


def input_symbols(matrix):
    symbols = set()
    for element in matrix:
        if not element.isnumeric() and element != '.':
            symbols.add(element)
    return symbols


def input_gears(matrix):
    gears = {}
    for i, j in matrix.coordinates:
        if matrix[i][j] == '*':
            gears[(i, j)] = list()
    return gears


def solution_1():
    matrix = read_input()
    symbols = input_symbols(matrix)

    result = 0

    builder = NumberBuilder()
    for i, j in matrix.coordinates:
        if matrix[i][j].isnumeric():
            builder.append(matrix[i][j], (i, j))
            next = matrix.peek(i, j + 1)
            if next is None or not next.isnumeric():
                for i, j in neighbor_coordinates(builder.number_coordinates):
                    if matrix.peek(i, j) in symbols:
                        result += int(builder.number)
                        break
                builder = NumberBuilder()
    return result


def solution_2():
    matrix = read_input()
    gears = input_gears(matrix)

    builder = NumberBuilder()
    for i, j in matrix.coordinates:
        if matrix[i][j].isnumeric():
            builder.append(matrix[i][j], (i, j))
            next = matrix.peek(i, j + 1)
            if next is None or not next.isnumeric():
                for i, j in neighbor_coordinates(builder.number_coordinates):
                    if matrix.peek(i, j) == '*':
                        gears[(i, j)].append(int(builder.number))
                        break
                builder = NumberBuilder()

    result = 0
    for numbers in gears.values():
        if len(numbers) == 2:
            result += numbers[0] * numbers[1]
    return result


if __name__ == '__main__':
    print('--- Day 3: Gear Ratios ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
