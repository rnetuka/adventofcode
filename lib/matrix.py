from .matrix_row import Row
from .matrix_column import Column
from .matrix_iterators import ElementIterator
from .matrix_iterators import CoordinatesIterable


class Matrix:

    def __init__(self, rows, columns, default=0):
        self.width = columns
        self.height = rows
        self.elements = [[default] * self.width for _ in range(self.height)]

    @staticmethod
    def parse(string):
        lines = [line for line in string.split('\n') if line]
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
            return Matrix.parse(file.read())

    @property
    def rows(self):
        return [self.row(i) for i in range(self.height)]

    def row(self, i):
        if i < 0 or i >= self.height:
            return None
        return Row(self.elements[i])

    @property
    def columns(self):
        return [self.column(j) for j in range(self.width)]

    def column(self, j):
        return Column(self, j)

    def peek(self, i, j=None):
        if isinstance(i, tuple) and len(i) == 2:
            i, j = i[0], i[1]

        if i < 0 or i >= self.height or j < 0 or j >= self.width:
            return None

        return self.elements[i][j]

    def insert_row(self, i, elements):
        if len(elements) != self.width:
            raise Exception('Row must have the same width as the matrix')

        self.elements.insert(i, list(elements))
        self.height += 1

    def insert_column(self, j, elements):
        if len(elements) != self.height:
            raise Exception('Column must have the same height as the matrix')

        for i in range(self.height):
            self.elements[i].insert(j, elements[i])
        self.width += 1

    @property
    def coordinates(self):
        return CoordinatesIterable(self)

    def __getitem__(self, i):
        if isinstance(i, tuple) and len(i) == 2:
            i, j = i[0], i[1]
            return self.elements[i][j]
        return Row(self.elements[i])

    def __iter__(self):
        return ElementIterator(self)

    def __repr__(self):
        repr = ''
        for row in range(self.height):
            repr += ''.join(str(self[row]))
            repr += '\n'
        return repr
