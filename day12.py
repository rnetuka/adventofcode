def arrangements(string, occurrences, acc='', state='CONSUME_CHARS_STATE', count=0):
    while True:
        if len(string) == 0:
            if len(occurrences) == 0 and count == 0:
                return 1
            if len(occurrences) == 1:
                return count == occurrences[0]
            return 0
        next_char = string.pop(0)
        acc += next_char
        if next_char == '#':
            state = 'CHECK_OCCURRENCES_STATE'
            count += 1
        if next_char == '.':
            if state == 'CHECK_OCCURRENCES_STATE':
                if len(occurrences) == 0:
                    return 0
                next_count = occurrences.pop(0)
                if count != next_count:
                    return 0
                state = 'CONSUME_CHARS_STATE'
                count = 0
        if next_char == '?':
            acc = acc[:-1]
            return arrangements(['.'] + list(string), list(occurrences), acc, state, count) \
                   + arrangements(['#'] + list(string), list(occurrences), acc, state, count)


def unfold(string, occurrences):
    s = string
    for i in range(4):
        s += '?'
        s += string
    return s, occurrences * 5


def solution_1():
    c = 0
    with open('input/day12.txt') as file:
        for line in file.readlines():
            parts = line.split(' ')
            string = parts[0]
            occurrences = [int(i) for i in parts[1].split(',')]
            c += arrangements([*string], occurrences)

    return c


def solution_2():
    c = 0
    with open('input/day12.txt') as file:
        for line in file.readlines():
            parts = line.split(' ')
            string = parts[0]
            occurrences = [int(i) for i in parts[1].split(',')]
            s, o = unfold(string, occurrences)
            c += arrangements([*s], o)

    return c


if __name__ == '__main__':
    print(solution_1())
    print(solution_2())
