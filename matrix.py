from models import Edge, EdgeType, normalize_weight


class MatrixParseError(ValueError):
    def __init__(self, code):
        super().__init__(code)
        self.code = code


def parse_int_matrix(text):
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if not lines:
        raise MatrixParseError("format")

    try:
        matrix = [list(map(int, line.split())) for line in lines]
    except ValueError as exc:
        raise MatrixParseError("format") from exc

    if not matrix or not matrix[0]:
        raise MatrixParseError("format")
    if any(len(row) != len(matrix[0]) for row in matrix):
        raise MatrixParseError("size")

    return matrix


def parse_adjacency_matrix(text):
    try:
        matrix = parse_int_matrix(text)
    except MatrixParseError as exc:
        if exc.code == "size":
            raise MatrixParseError("square") from exc
        raise
    if len(matrix) != len(matrix[0]):
        raise MatrixParseError("square")
    if any(value < 0 for row in matrix for value in row):
        raise MatrixParseError("format")
    return matrix


def parse_incidence_matrix(text):
    matrix = parse_int_matrix(text)
    for col in range(len(matrix[0])):
        values = [matrix[row][col] for row in range(len(matrix)) if matrix[row][col] != 0]
        if len(values) > 2:
            raise MatrixParseError("size")
        if len(values) == 2 and abs(values[0]) != abs(values[1]):
            raise MatrixParseError("format")
    return matrix


def edges_from_adjacency_matrix(matrix):
    edges = []
    for start_index, row in enumerate(matrix):
        for end_index, weight in enumerate(row):
            if weight <= 0:
                continue

            opposite_index = find_directed_edge(edges, end_index, start_index, weight)
            if opposite_index != -1:
                edges[opposite_index] = Edge(end_index, start_index, weight, EdgeType.UNDIRECTED)
            else:
                edges.append(Edge(start_index, end_index, weight, EdgeType.DIRECTED))
    return edges


def edges_from_incidence_matrix(matrix):
    edges = []
    row_count = len(matrix)
    column_count = len(matrix[0])

    for col in range(column_count):
        values = [
            (row, matrix[row][col])
            for row in range(row_count)
            if matrix[row][col] != 0
        ]
        if len(values) == 1:
            row, weight = values[0]
            edges.append(Edge(row, row, abs(weight), EdgeType.DIRECTED))
        elif len(values) == 2:
            first_row, first_weight = values[0]
            second_row, second_weight = values[1]
            weight = abs(first_weight)

            if first_weight == second_weight:
                edges.append(Edge(first_row, second_row, weight, EdgeType.UNDIRECTED))
            elif first_weight > 0:
                edges.append(Edge(first_row, second_row, weight, EdgeType.DIRECTED))
            else:
                edges.append(Edge(second_row, first_row, weight, EdgeType.DIRECTED))
    return edges


def adjacency_matrix(vertex_count, edges):
    matrix = [[0] * vertex_count for _ in range(vertex_count)]
    for edge in valid_edges(vertex_count, edges):
        weight = normalize_weight(edge.weight)
        matrix[edge.start_index][edge.end_index] = weight
        if edge.edge_type == EdgeType.UNDIRECTED:
            matrix[edge.end_index][edge.start_index] = weight
    return matrix


def incidence_matrix(vertex_count, edges):
    edges = valid_edges(vertex_count, edges)
    matrix = [[0] * len(edges) for _ in range(vertex_count)]

    for col, edge in enumerate(edges):
        weight = normalize_weight(edge.weight)
        if edge.edge_type == EdgeType.DIRECTED:
            matrix[edge.start_index][col] = weight
            matrix[edge.end_index][col] = -weight
        else:
            matrix[edge.start_index][col] = weight
            matrix[edge.end_index][col] = weight
    return matrix


def format_matrix(matrix):
    if not matrix or not matrix[0]:
        return ""
    max_len = max(len(str(value)) for row in matrix for value in row)
    return "\n".join("  ".join(f"{value:>{max_len}}" for value in row) for row in matrix)


def edge_headers(edges):
    return [f"{edge.start_index + 1}-{edge.end_index + 1}" for edge in edges]


def valid_edges(vertex_count, edges):
    return [
        edge for edge in edges
        if 0 <= edge.start_index < vertex_count and 0 <= edge.end_index < vertex_count
    ]


def find_directed_edge(edges, start_index, end_index, weight):
    for index, edge in enumerate(edges):
        if (
            edge.start_index == start_index
            and edge.end_index == end_index
            and edge.weight == weight
            and edge.edge_type == EdgeType.DIRECTED
        ):
            return index
    return -1
