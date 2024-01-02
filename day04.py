import re


class Card:

    def __init__(self):
        self.id = None
        self.winning_numbers = []
        self.numbers = []

    @staticmethod
    def parse(string):
        match = re.match('Card\\s+([0-9]+):([0-9\\s]+)\\|([0-9\\s]+)', string)
        card = Card()
        card.id = int(match.group(1))
        card.winning_numbers = [int(n) for n in match.group(2).split()]
        card.numbers = [int(n) for n in match.group(3).split()]
        return card

    @property
    def matches(self):
        matches = 0
        for n in self.numbers:
            if n in self.winning_numbers:
                matches += 1
        return matches

    @property
    def wins(self):
        wins = set()
        for i in range(1, self.matches + 1):
            wins.add(self.id + i)
        return wins

    @property
    def value(self):
        value = 0
        for n in self.numbers:
            if n in self.winning_numbers:
                if value == 0:
                    value = 1
                else:
                    value *= 2
        return value


def read_cards():
    cards = []
    with open('input/day04.txt') as file:
        for line in file.readlines():
            cards.append(Card.parse(line))
    return cards


def solution_1():
    n = 0
    for card in read_cards():
        n += card.value
    return n


def solution_2():
    cards = {}
    cache = {}

    def process(card):
        if card.id in cache:
            return cache[card.id]

        if card.matches == 0:
            cache[card.id] = 0
            return 0

        n = 0
        for win in card.wins:
            n += 1
            n += process(cards[win])
        cache[card.id] = n
        return n

    for card in read_cards():
        cards[card.id] = card

    n = 0
    for card in cards.values():
        n += 1
        n += process(card)

    return n


if __name__ == '__main__':
    print('--- Day 4: Scratchcards ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
