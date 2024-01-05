class Interpreter:

    def __init__(self):
        self.rules = {}
        self.variables = {}

    def add_rule(self, rule):
        name = rule[:rule.index('{')]
        parts = rule[rule.index('{')+1:rule.index('}')].split(',')
        self.rules[name] = parts

    def apply_rule(self, rule):
        parts = self.rules[rule]
        for i in range(len(parts) - 1):
            part = parts[i]
            condition, command = part.split(':')
            if '<' in condition:
                variable, value = condition.split('<')
                if self.variables[variable] < int(value):
                    return command
            elif '>' in condition:
                variable, value = condition.split('>')
                if self.variables[variable] > int(value):
                    return command
        return parts[-1]

    def run(self):
        rule = 'in'
        while True:
            rule = self.apply_rule(rule)
            if rule == 'A':
                return self.variables['x'] + self.variables['m'] + self.variables['a'] + self.variables['s']
            if rule == 'R':
                return 0


def solution_1():
    interpreter = Interpreter()
    n = 0
    with open('input/day19.txt') as file:
        for line in file.readlines():
            line = line.strip()
            if line.startswith('{'):
                interpreter.variables = {}
                for assignment in line[1:-1].split(','):
                    name, value = assignment.split('=')
                    interpreter.variables[name] = int(value)
                n += interpreter.run()
            elif line:
                interpreter.add_rule(line)

    return n


if __name__ == '__main__':
    print('--- Day 19: Aplenty ---')
    print(f'Part 1: {solution_1()}')
