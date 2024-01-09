from lib.interval import Interval


MIN_VALUE = 1
MAX_VALUE = 4000

operations = {
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b
}


def infinite_interval():
    return Interval(MIN_VALUE, MAX_VALUE)


class Condition:

    def __init__(self, variable, operation, value):
        self.variable = variable
        self.operation = operation
        self.value = value

    @staticmethod
    def parse(string):
        # no need to check for <= or >= since these two operations are created only through negation of existing
        # condition
        if '<' in string:
            variable, value = string.split('<')
            return Condition(variable, '<', int(value))
        if '>' in string:
            variable, value = string.split('>')
            return Condition(variable, '>', int(value))

    @staticmethod
    def true():
        return Condition(variable=None, operation=None, value=True)

    @property
    def is_true(self):
        return self.variable is None and self.value is True

    def check(self, variables):
        if self.is_true:
            return True
        else:
            operand_a = variables[self.variable]
            operand_b = self.value
            return operations[self.operation](operand_a, operand_b)

    def create_interval(self):
        """Create an interval for checked variable that satisfies the condition"""
        if self.is_true:
            return infinite_interval()
        elif self.operation == '<':
            return Interval(MIN_VALUE, self.value - 1)
        elif self.operation == '>':
            return Interval(self.value + 1, MAX_VALUE)
        elif self.operation == '<=':
            return Interval(MIN_VALUE, self.value)
        elif self.operation == '>=':
            return Interval(self.value, MAX_VALUE)

    def __repr__(self):
        return 'True' if self.is_true else ' '.join([self.variable, self.operation, str(self.value)])


def negated(condition):
    if condition.operation == '<':
        return Condition(condition.variable, '>=', condition.value)
    if condition.operation == '>':
        return Condition(condition.variable, '<=', condition.value)


class ConditionChain:

    def __init__(self):
        self.conditions = []

    def check(self, variables):
        result = True
        for condition in self.conditions:
            result = result and condition.check(variables)
        return result

    def __repr__(self):
        return ' AND '.join(str(condition) for condition in self.conditions)


class Branch:

    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    @staticmethod
    def parse(string):
        if ':' in string:
            condition, body = string.split(':')
            return Branch(condition=Condition.parse(condition), body=body)
        else:
            return Branch(condition=Condition.true(), body=string)

    @staticmethod
    def parse_if_branch(strings):
        return Branch.parse(strings[0])

    @staticmethod
    def parse_elif_branch(strings, i):
        chain = ConditionChain()
        for j in range(i):
            other_branch = Branch.parse(strings[j])
            chain.conditions.append(negated(other_branch.condition))
        branch = Branch.parse(strings[i])
        chain.conditions.append(branch.condition)
        branch.condition = chain
        return branch

    @staticmethod
    def parse_else_branch(strings):
        chain = ConditionChain()
        for j in range(len(strings) - 1):
            other_branch = Branch.parse(strings[j])
            chain.conditions.append(negated(other_branch.condition))
        branch = Branch.parse(strings[-1])
        branch.condition = chain
        return branch

    def __repr__(self):
        return 'if ' + str(self.condition) + ': ' + self.body


class Interpreter:

    def __init__(self):
        self.rules = {}
        self.variables = {}

    def add_rule(self, rule):
        name = rule[:rule.index('{')]
        parts = rule[rule.index('{')+1:rule.index('}')].split(',')
        branches = []
        branches.append(Branch.parse_if_branch(parts))
        for i, part in enumerate(parts):
            if 0 < i < len(parts) - 1:
                branches.append(Branch.parse_elif_branch(parts, i))
        branches.append(Branch.parse_else_branch(parts))
        self.rules[name] = branches

    def apply_rule(self, rule):
        branches = self.rules[rule]
        for i in range(len(branches) - 1):
            branch = branches[i]
            if branch.condition.check(self.variables):
                return branch.body
        return branches[-1].body

    def run(self):
        current = 'in'
        while True:
            current = self.apply_rule(current)
            if current == 'A':
                return self.variables['x'] + self.variables['m'] + self.variables['a'] + self.variables['s']
            if current == 'R':
                return 0


def branch_nodes_for(interpreter, rule, conditions):
    branches = []
    rhs = interpreter.rules[rule]
    for branch in rhs:
        branches.append({'conditions': conditions + [branch.condition], 'next': branch.body})
    return branches


def aggregate(conditions):
    intervals = {'x': infinite_interval(), 'm': infinite_interval(), 'a': infinite_interval(), 's': infinite_interval()}
    for condition in conditions:
        if isinstance(condition, ConditionChain):
            for sub_condition in condition.conditions:
                interval = sub_condition.create_interval()
                intervals[sub_condition.variable] = intervals[sub_condition.variable].intersect(interval)
        else:
            interval = condition.create_interval()
            intervals[condition.variable] = intervals[condition.variable].intersect(interval)
    return intervals


def create_interpreter():
    interpreter = Interpreter()

    with open('input/day19.txt') as file:
        for line in file.readlines():
            if line.strip() and not line.startswith('{'):
                interpreter.add_rule(line)

    return interpreter


def solution_1():
    interpreter = create_interpreter()
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
    return n


def solution_2():
    interpreter = create_interpreter()
    n = 0
    queue = [{'next': 'in', 'conditions': []}]
    while queue:
        node = queue.pop(0)
        conditions = node['conditions']
        rule = node['next']
        if rule == 'A':
            intervals = aggregate(conditions)
            m = len(intervals['x']) * len(intervals['m']) * len(intervals['a']) * len(intervals['s'])
            n += m
        elif rule == 'R':
            continue
        else:
            queue += branch_nodes_for(interpreter, rule, conditions)
    return n


if __name__ == '__main__':
    print('--- Day 19: Aplenty ---')
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
