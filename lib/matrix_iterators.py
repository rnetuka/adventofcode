class ElementIterator:

    def __init__(self, matrix):
        self.matrix = matrix
        self.i = 0
        self.j = 0

    def __next__(self):
        item = self.matrix[self.i][self.j]
        self.j += 1
        if self.j >= self.matrix.width:
            self.i += 1
            self.j = 0
        if self.i >= self.matrix.height:
            raise StopIteration
        return item


class CoordinatesIterator:

    def __init__(self, matrix):
        self.matrix = matrix
        self.i = 0
        self.j = 0

    def __next__(self):
        result_i = self.i
        result_j = self.j
        self.j += 1
        if self.j >= self.matrix.width:
            self.i += 1
            self.j = 0
        if result_i >= self.matrix.height:
            raise StopIteration
        return result_i, result_j


class CoordinatesIterable:

    def __init__(self, matrix):
        self.iterator = CoordinatesIterator(matrix)

    def __iter__(self):
        return self.iterator
