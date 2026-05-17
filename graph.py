from models import Edge, EdgeType, Vertex, normalize_weight


class Graph:
    def __init__(self):
        self.vertices = []
        self.edges = []

    def clear(self):
        self.vertices.clear()
        self.edges.clear()

    def replace(self, vertices, edges):
        self.vertices = list(vertices)
        self.edges = [Edge(edge.start_index, edge.end_index, edge.weight, edge.edge_type) for edge in edges]

    def add_vertex(self, x, y, weight=1):
        self.vertices.append(Vertex(x, y, weight))

    def move_vertex(self, index, x, y):
        if self.has_vertex(index):
            self.vertices[index].x = x
            self.vertices[index].y = y

    def delete_vertex(self, index):
        if not self.has_vertex(index):
            return

        self.vertices.pop(index)
        self.edges = [
            edge for edge in self.edges
            if edge.start_index != index and edge.end_index != index
        ]

        for edge in self.edges:
            if edge.start_index > index:
                edge.start_index -= 1
            if edge.end_index > index:
                edge.end_index -= 1

    def add_edge(self, start_index, end_index, weight=1, edge_type=EdgeType.UNDIRECTED):
        if not self.has_vertex(start_index) or not self.has_vertex(end_index):
            return

        edge_type = EdgeType.from_value(edge_type)
        weight = normalize_weight(weight)
        self.edges = [
            edge for edge in self.edges
            if not self._is_same_connection(edge, start_index, end_index, edge_type)
        ]
        self.edges.append(Edge(start_index, end_index, weight, edge_type))

    def valid_edges(self):
        return [
            edge for edge in self.edges
            if self.has_vertex(edge.start_index) and self.has_vertex(edge.end_index)
        ]

    def has_vertex(self, index):
        return 0 <= index < len(self.vertices)

    @staticmethod
    def _is_same_connection(edge, start_index, end_index, edge_type):
        same_direction = edge.start_index == start_index and edge.end_index == end_index
        opposite_direction = edge.start_index == end_index and edge.end_index == start_index

        if edge.edge_type == edge_type:
            return same_direction or (edge_type == EdgeType.UNDIRECTED and opposite_direction)
        return same_direction or opposite_direction
