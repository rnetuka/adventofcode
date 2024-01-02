FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

card_strengths = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}


class HandOfCards:

    def __init__(self, cards):
        self.cards = cards

    def replace_jokers(self):
        if 'J' not in self.cards:
            return self.cards

        if self.cards == 'JJJJJ':
            return self.cards

        card_counts = {}
        for card in set(self.cards):
            if card != 'J':
                card_counts[card] = self.cards.count(card)
        picked = max(card_counts, key=card_counts.get)
        return self.cards.replace('J', picked)

    @property
    def type(self):
        cards = self.replace_jokers()
        counts = [cards.count(card) for card in set(cards)]

        if 5 in counts:
            return FIVE_OF_A_KIND

        if 4 in counts:
            return FOUR_OF_A_KIND

        if 3 in counts and 2 in counts:
            return FULL_HOUSE

        if 3 in counts:
            return THREE_OF_A_KIND

        if counts.count(2) == 2:
            return TWO_PAIR

        if 2 in counts:
            return ONE_PAIR

        return HIGH_CARD

    def __lt__(self, other):
        if self.type == other.type:
            for i in range(len(self.cards)):
                s1 = card_strengths[self.cards[i]]
                s2 = card_strengths[other.cards[i]]
                if s1 < s2:
                    return True
                if s1 > s2:
                    return False
            # hands must be equal at this point
            return False
        return self.type < other.type


def read_input():
    with open('input/day07.txt') as file:
        hands = []
        bids = {}
        for line in file.readlines():
            parts = line.split()
            hands.append(HandOfCards(parts[0]))
            bids[parts[0]] = int(parts[1])
        return hands, bids


def solution_1():
    hands, bids = read_input()
    hands = sorted(hands)
    n = 0
    for i, hand in enumerate(hands):
        n += bids[hand.cards] * (i + 1)
    return n


def solution_2():
    hands, bids = read_input()
    card_strengths['J'] = 1
    hands = sorted(hands)
    n = 0
    for i, hand in enumerate(hands):
        n += bids[hand.cards] * (i + 1)
    return n


if __name__ == '__main__':
    print('--- Day 7: Camel Cards ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('Part 2: ', end='')
    print(solution_2())
