import sys
from lib.interval import Interval


input_path = 'input/day05.txt'


class Formula:

    def __init__(self, interval, increment):
        self.interval = interval
        self.increment = increment

    @staticmethod
    def parse(string):
        parts = [int(n) for n in string.split(' ')]
        destination_range_start = parts[0]
        source_range_start = parts[1]
        range_length = parts[2]
        interval = Interval(source_range_start, source_range_start + range_length - 1)
        increment = destination_range_start - source_range_start
        return Formula(interval, increment)

    def __lt__(self, other):
        return self.interval < other.interval


class Chapter:

    def __init__(self, number):
        self.number = number
        self.formulas = []

    def complete(self):
        self.formulas = sorted(self.formulas)
        if not self.formulas:
            self.formulas = [Formula(Interval(0, sys.maxsize), 0)]
        else:
            new_formulas = []
            last_i = 0
            for mapping in self.formulas:
                if mapping.interval.start > last_i:
                    new_interval = Interval(last_i, mapping.interval.start - 1)
                    new_formula = Formula(new_interval, 0)
                    new_formulas.append(new_formula)

                new_formulas.append(mapping)
                last_i = mapping.interval.end + 1

            last = new_formulas[-1]
            if last.interval.end < sys.maxsize:
                new_interval = Interval(last.interval.end + 1, sys.maxsize)
                new_formula = Formula(new_interval, 0)
                new_formulas.append(new_formula)

            self.formulas = new_formulas

    def increment_for(self, value):
        for formula in self.formulas:
            if value in formula.interval:
                return formula.increment


class Almanac:

    def __init__(self):
        self.chapters = {}

    @staticmethod
    def from_file(path=input_path):
        with open(path) as file:
            almanac = Almanac()
            chapter = None
            chapter_number = 0
            for line in file.read().splitlines():
                if line.startswith('seeds:'):
                    pass
                elif 'map:' in line:
                    chapter = line.strip()
                    chapter = chapter.rstrip(':')
                    almanac.chapters[chapter] = Chapter(chapter_number)
                    chapter_number += 1
                elif len(line.strip()) == 0 and chapter is not None:
                    almanac.chapters[chapter].complete()
                    chapter = None
                elif chapter is not None:
                    formula = Formula.parse(line)
                    almanac.chapters[chapter].formulas.append(formula)
            if chapter is not None:
                almanac.chapters[chapter].complete()
            return almanac

    def apply(self, values, chapter):
        chapter = self.chapters[chapter]
        new_values = []
        for interval in values:
            for formula in chapter.formulas:
                intersection = interval.intersect(formula.interval)
                if intersection:
                    new_interval = Interval(intersection.start + formula.increment, intersection.end + formula.increment)
                    new_values.append(new_interval)
        return new_values


def read_seeds():
    with open(input_path) as file:
        line = file.readline()
        if line.startswith('seeds:'):
            rest = line[line.index(':') + 1:].strip()
            return [int(n) for n in rest.split(' ')]


def read_seed_intervals():
    values = read_seeds()
    intervals = []
    for i in range(0, len(values), 2):
        interval = Interval(values[i], values[i] + values[i + 1] - 1)
        intervals.append(interval)
    return intervals


def solution_1():
    seeds = read_seeds()
    almanac = Almanac.from_file()
    locations = []
    for value in seeds:
        value += almanac.chapters['seed-to-soil map'].increment_for(value)
        value += almanac.chapters['soil-to-fertilizer map'].increment_for(value)
        value += almanac.chapters['fertilizer-to-water map'].increment_for(value)
        value += almanac.chapters['water-to-light map'].increment_for(value)
        value += almanac.chapters['light-to-temperature map'].increment_for(value)
        value += almanac.chapters['temperature-to-humidity map'].increment_for(value)
        value += almanac.chapters['humidity-to-location map'].increment_for(value)
        locations.append(value)
    return min(locations)


def solution_2():
    seed_intervals = read_seed_intervals()
    almanac = Almanac.from_file()
    values = seed_intervals
    values = almanac.apply(values, 'seed-to-soil map')
    values = almanac.apply(values, 'soil-to-fertilizer map')
    values = almanac.apply(values, 'fertilizer-to-water map')
    values = almanac.apply(values, 'water-to-light map')
    values = almanac.apply(values, 'light-to-temperature map')
    values = almanac.apply(values, 'temperature-to-humidity map')
    values = almanac.apply(values, 'humidity-to-location map')
    return min([interval.start for interval in values])


if __name__ == '__main__':
    print('--- Day 5: If You Give A Seed A Fertilizer ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
