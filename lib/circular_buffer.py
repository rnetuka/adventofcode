class CircularBuffer:

    def __init__(self, elements):
        self.elements = list(elements)

    def index(self, element):
        return self.elements.index(element)

    def __getitem__(self, i):
        if i >= len(self.elements):
            i %= len(self.elements)
        return self.elements[i]

    def __iter__(self):
        return CircularBufferIterator(self)


class CircularBufferIterator:

    def __init__(self, buffer):
        self.buffer = buffer
        self.i = 0

    def __next__(self):
        if self.i >= len(self.buffer.elements):
            self.i = 0
        element = self.buffer.elements[self.i]
        self.i += 1
        return element
