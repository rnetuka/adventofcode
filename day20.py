class Circuit:

    def __init__(self):
        self.modules = {}
        self.pulses = {0: 0, 1: 0}
        self.queue = []
        self.pushes = 0
        self.input_modules_for_rx = []
        self.amplitude = {'dr': None, 'cl': None, 'bm': None, 'tn': None}

    @staticmethod
    def from_file(path):
        with open(path) as file:
            return Circuit.parse(file.read().strip())

    @staticmethod
    def parse(string):
        circuit = Circuit()
        for line in string.split('\n'):
            name, outputs = line.split(' -> ')
            if name == 'broadcaster':
                module = BroadcastModule(circuit)
                module.outputs = outputs.split(', ')
                circuit.modules[name] = module

            if name.startswith('%'):
                name = name[1:]
                module = FlipFlop(name, circuit)
                module.outputs = outputs.split(', ')
                circuit.modules[name] = module

            if name.startswith('&'):
                name = name[1:]
                module = Conjunction(name, circuit)
                module.outputs = outputs.split(', ')
                circuit.modules[name] = module

        for module in circuit.modules:
            for output in circuit.modules[module].outputs:
                if output in circuit.modules and isinstance(circuit.modules[output], Conjunction):
                    circuit.modules[output].connect_input(module)

        for module in circuit.modules:
            if 'rx' in circuit.modules[module].outputs:
                conjunction = module
                circuit.input_modules_for_rx = circuit.modules[conjunction].remembered.keys()
                break

        return circuit

    def send(self, source, destination, pulse):
        self.pulses[pulse] += 1
        self.queue.append((source, destination, pulse))
        if source in self.input_modules_for_rx and pulse == 1:
            self.amplitude[source] = self.pushes

    def push_button(self):
        self.pushes += 1
        self.send('button', 'broadcaster', 0)
        while self.queue:
            source, destination, pulse = self.queue.pop(0)
            if destination in self.modules:
                self.modules[destination].process(source, pulse)


class Module:

    def __init__(self, name, circuit):
        self.name = name
        self.circuit = circuit
        self.outputs = []

    def send(self, pulse):
        for output in self.outputs:
            self.circuit.send(self.name, output, pulse)


class FlipFlop(Module):

    def __init__(self, name, circuit):
        super().__init__(name, circuit)
        self.on = False

    def process(self, input, signal):
        if signal == 0:
            if self.on:
                self.on = False
                self.send(0)
            else:
                self.on = True
                self.send(1)

    def __repr__(self):
        return '%' + self.name + ' -> ' + ', '.join(self.outputs)


class Conjunction(Module):

    def __init__(self, name, circuit):
        super().__init__(name, circuit)
        self.remembered = {}

    def connect_input(self, input):
        self.remembered[input] = 0

    def process(self, input, pulse):
        self.remembered[input] = pulse
        if all(pulse == 1 for pulse in self.remembered.values()):
            self.send(0)
        else:
            self.send(1)

    def __repr__(self):
        return '&' + self.name + ' -> ' + ', '.join(self.outputs) + ' (inputs:' + ', '.join(self.remembered.keys()) + ')'


class BroadcastModule(Module):

    def __init__(self, circuit):
        super().__init__('broadcaster', circuit)

    def process(self, input, pulse):
        self.send(pulse)

    def __repr__(self):
        return 'broadcaster -> ' + ', '.join(self.outputs)


def solution_1():
    circuit = Circuit.from_file('input/day20.txt')
    for _ in range(1000):
        circuit.push_button()
    return circuit.pulses[0] * circuit.pulses[1]


def solution_2():
    circuit = Circuit.from_file('input/day20.txt')
    while True:
        circuit.push_button()
        if all(circuit.amplitude[module] is not None for module in circuit.input_modules_for_rx):
            n = 1
            for module in circuit.input_modules_for_rx:
                n *= circuit.amplitude[module]
            return n


if __name__ == '__main__':
    print('--- Day 20: Pulse Propagation ---')
    print(f'Part 1: {solution_1()}')
    print(f'Part 2: {solution_2()}')
