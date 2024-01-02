from .graph_algorithm import DijkstrasAlgorithm


class Edge:

    def __init__(self, a, b, length):
        self.a = a
        self.b = b
        self.length = length

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.length == other.length

    def __hash__(self):
        return hash((self.a, self.b, self.length))

    def __repr__(self):
        return repr(self.a) + ' -> ' + repr(self.b)


class Graph:

    def __init__(self):
        self.nodes = set()
        self.edges = set()
        self.algorithm = DijkstrasAlgorithm(self)

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, a, b, length=1):
        self.edges.add(Edge(a, b, length))
        self.edges.add(Edge(b, a, length))

    def neighbors_of(self, node):
        neighbors = set()
        for edge in self.edges:
            if edge.a == node:
                neighbors.add(edge.b)
        return neighbors

    def edge_between(self, a, b):
        for edge in self.edges:
            if edge.a == a and edge.b == b:
                return edge
