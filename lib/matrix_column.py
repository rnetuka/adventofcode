class Column:

    def __init__(self, matrix, j):
        self.matrix = matrix
        self.j = j

    def __getitem__(self, i):
        return self.matrix[i][self.j]

    def __setitem__(self, i, value):
        self.matrix[i][self.j] = value

    def __repr__(self):
        repr = ''
        for i in range(self.matrix.height):
            repr += str(self.matrix[i][self.j])
            repr += '\n'
        return repr
