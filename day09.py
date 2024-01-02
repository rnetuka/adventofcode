sequences = []


class Sequence:

    def __init__(self, elements):
        self.elements = elements

    @staticmethod
    def parse(string):
        return Sequence([int(n) for n in string.split()])

    def differences(self):
        diffs = []
        for i in range(1, len(self.elements)):
            diffs.append(self.elements[i] - self.elements[i - 1])
        return diffs


def extrapolate(sequence, i):
    if all([d == 0 for d in sequence.elements]):
        return 0
    else:
        diffs = sequence.differences()
        d = extrapolate(Sequence(diffs), i)
        # if extrapolating sequence beginning, use -d
        if i == 0:
            d *= -1
        return sequence.elements[i] + d


def solution_1():
    n = 0
    for sequence in sequences:
        n += extrapolate(sequence, i=-1)
    return n


def solution_2():
    n = 0
    for sequence in sequences:
        n += extrapolate(sequence, i=0)
    return n


if __name__ == '__main__':
    with open('input/day09.txt') as file:
        for line in file.readlines():
            sequences.append(Sequence.parse(line))

    print('--- Day 9: Mirage Maintenance ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('--- Part Two ---')
    print('Part 2: ', end='')
    print(solution_2())
