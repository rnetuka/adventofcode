import re


def get_number(string, color):
    match = re.search('([0-9]+) ' + color, string)
    return int(match.group(1)) if match else 0


class Round:

    def __init__(self):
        self.reds = 0
        self.blues = 0
        self.greens = 0

    @staticmethod
    def parse(string):
        round = Round()
        round.reds = get_number(string, 'red')
        round.blues = get_number(string, 'blue')
        round.greens = get_number(string, 'green')
        return round

    def is_possible(self):
        return self.reds <= 12 and self.greens <= 13 and self.blues <= 14


class Game:

    def __init__(self):
        self.id = None
        self.rounds = []

    @staticmethod
    def parse(string):
        match = re.search('Game ([0-9]+): (.*)$', string)
        game = Game()
        game.id = int(match.group(1))
        game.rounds = [Round.parse(s) for s in match.group(2).split(';')]
        return game

    def is_possible(self):
        return all(round.is_possible() for round in self.rounds)

    def required(self, color):
        return max([getattr(round, color) for round in self.rounds])


def read_input():
    with open('input/day02.txt') as file:
        return file.readlines()


def read_games():
    return [Game.parse(line) for line in read_input()]


def solution_1():
    n = 0
    for game in read_games():
        if game.is_possible():
            n += game.id
    return n


def solution_2():
    n = 0
    for game in read_games():
        n += game.required('reds') * game.required('greens') * game.required('blues')
    return n


if __name__ == '__main__':
    print('--- Day 2: Cube Conundrum ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
