import math
from collections import namedtuple
from lib.circular_buffer import CircularBuffer

Node = namedtuple('Node', ['left', 'right'])


def parse_node(string):
    parts = string.split(' = ')
    name = parts[0]
    parts = parts[1].split(', ')
    left = parts[0][1:]
    right = parts[1][:-1]
    return name, Node(left, right)


nodes = {}
instructions = ''


def navigate(start, finish_check):
    queue = CircularBuffer(list(instructions))
    node = start
    steps = 0

    for instruction in queue:
        if instruction == 'L':
            node = nodes[node].left
        elif instruction == 'R':
            node = nodes[node].right
        steps += 1
        if finish_check(node):
            break
    return steps


def solution_1():
    return navigate('AAA', lambda x: x == 'ZZZ')


def solution_2():
    starting_nodes = [node for node in nodes if node.endswith('A')]
    steps = []
    for node in starting_nodes:
        steps.append(navigate(node, lambda x: x.endswith('Z')))

    return math.lcm(*steps)


if __name__ == '__main__':
    with open('input/day08.txt') as file:
        instructions = file.readline().strip()
        for line in file.readlines():
            if line.strip():
                name, node = parse_node(line.strip())
                nodes[name] = node

    print('--- Day 8: Haunted Wasteland ---')
    print('Part 1: ', end='')
    print(solution_1())
    print('--- Part Two ---')
    print('Part 2: ', end='')
    print(solution_2())
