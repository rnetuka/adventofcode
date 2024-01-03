class Light:

    def __init__(self):
        self.boxes = {}
        for i in range(256):
            self.boxes[i] = {}

    def process(self, step):
        if '=' in step:
            label, focal_length = step.split('=')
            h = hash(label)
            self.boxes[h][label] = focal_length
        elif '-' in step:
            label = step[:-1]
            h = hash(label)
            if label in self.boxes[h]:
                del self.boxes[h][label]

    @property
    def focusing_power(self):
        p = 0
        for i in range(256):
            for j, label in enumerate(self.boxes[i].keys()):
                m = 1 + i
                m *= j + 1
                m *= int(self.boxes[i][label])
                p += m
        return p


def hash(string):
    n = 0
    for char in string:
        n += ord(char)
        n *= 17
        n %= 256
    return n


def solution_1():
    with open('input/day15.txt') as file:
        string = file.read().strip()
        n = 0
        for step in string.split(','):
            n += hash(step)
        return n


def solution_2():
    with open('input/day15.txt') as file:
        string = file.read().strip()
    light = Light()
    for step in string.split(','):
        light.process(step)
    return light.focusing_power


if __name__ == '__main__':
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
