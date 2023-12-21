class CyclingQueue:

    def __init__(self, elements):
        self.elements = list(elements)

    def pop(self):
        element = self.elements.pop(0)
        self.elements.append(element)
        return element
