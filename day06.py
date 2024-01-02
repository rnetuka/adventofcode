import itertools
from lib.interval import Interval


def wins(button_time, time, record):
    speed = button_time
    distance = (time - button_time) * speed
    return distance > record


def possibilities_to_win_race(time, record):
    c = 0
    for hold_time in range(1, time - 1):
        speed = hold_time
        distance = (time - hold_time) * speed
        if distance > record:
            c += 1
    return c


def solution_1():
    with open('input/day06.txt') as file:
        times = [int(n) for n in file.readline().split()[1:]]
        records = [int(n) for n in file.readline().split()[1:]]
        n = 1
        for time, record in itertools.zip_longest(times, records):
            n *= possibilities_to_win_race(time, record)
        return n


def solution_2():
    with open('input/day06.txt') as file:
        time = int(''.join(file.readline().split()[1:]))
        record = int(''.join(file.readline().split()[1:]))

        n = m = time // 2
        while wins(n, time, record):
            n -= 10_000
        while not wins(n, time, record):
            n += 1
        while wins(m, time, record):
            m += 10_000
        while not wins(m, time, record):
            m -= 1
        return len(Interval(n, m))


if __name__ == '__main__':
    print('--- Day 6: Wait For It ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
