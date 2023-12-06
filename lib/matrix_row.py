class Row:

    def __init__(self, elements):
        self.elements = elements

    def __setitem__(self, j, value):
        self.elements[j] = value

    def __getitem__(self, j):
        return self.elements[j]

    def __repr__(self):
        return ''.join(self.elements)
