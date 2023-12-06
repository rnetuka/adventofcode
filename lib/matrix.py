from .matrix_row import Row
from .matrix_column import Column
from .matrix_iterators import ElementIterator
from .matrix_iterators import CoordinatesIterable


class Matrix:

    def __init__(self, rows, columns):
        self.width = columns
        self.height = rows
        self.elements = [[0] * self.width for _ in range(self.height)]

    @staticmethod
    def parse(string):
        lines = [line.rstrip() for line in string if line]
        rows = len(lines)
        columns = len(lines[0])
        matrix = Matrix(rows, columns)
        for i in range(matrix.height):
            for j in range(matrix.width):
                matrix[i][j] = lines[i][j]
        return matrix

    @staticmethod
    def from_file(path):
        with open(path) as file:
            return Matrix.parse(file.readlines())

    def row(self, i):
        return Row(self.elements[i])

    def column(self, j):
        return Column(self, j)

    def peek(self, i, j):
        if i < 0 or i >= self.height or j < 0 or j >= self.width:
            return None
        return self.elements[i][j]

    @property
    def coordinates(self):
        return CoordinatesIterable(self)

    def __getitem__(self, i):
        return Row(self.elements[i])

    def __iter__(self):
        return ElementIterator(self)

    def __repr__(self):
        repr = ''
        for row in range(self.height):
            repr += ''.join(self[row])
            repr += '\n'
        return repr
