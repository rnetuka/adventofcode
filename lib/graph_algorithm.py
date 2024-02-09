class DijkstrasAlgorithm:

    def __init__(self, graph):
        self.graph = graph

    def distances_from(self, start):
        distances = {}
        previous = {}
        unvisited = []

        for node in self.graph.nodes:
            distances[node] = float('inf')
            previous[node] = None
            unvisited.append(node)

        distances[start] = 0

        while len(unvisited) > 0:
            node = min(unvisited, key=lambda x: distances[x])
            unvisited.remove(node)

            for neighbor in self.graph.neighbors_of(node):
                if neighbor in unvisited:
                    alt = distances[node] + self.graph.edge_between(node, neighbor).length
                    if alt < distances[neighbor]:
                        distances[neighbor] = alt
                        previous[neighbor] = node

        return distances

    def shortest_path(self, start, finish):
        return self.distances_from(start)[finish]
