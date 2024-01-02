import regex


replacements = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8',
                'nine': '9'}


def read_input():
    with open('input/day01.txt') as file:
        return file.readlines()


def sum_calibration_values(pattern):
    result = 0
    for line in read_input():
        digits = regex.findall(pattern, line, overlapped=True)
        a = digits[0]
        b = digits[-1]
        n = int(digit(a) + digit(b))
        result += n
    return result


def solution_1():
    return sum_calibration_values(pattern='[0-9]')


def solution_2():
    return sum_calibration_values(pattern='[0-9]|one|two|three|four|five|six|seven|eight|nine')


def digit(word):
    return replacements[word] if word in replacements else word


if __name__ == '__main__':
    print('--- Day 1: Trebuchet?! ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
