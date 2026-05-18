import re

from models import Edge, EdgeType, normalize_weight


class MatrixParseError(ValueError):
    def __init__(self, code, row=None, column=None, value=None, expected=None, actual=None):
        super().__init__(code)
        self.code = code
        self.row = row
        self.column = column
        self.value = value
        self.expected = expected
        self.actual = actual


def parse_int_matrix(text):
    lines = normalized_matrix_lines(text)
    if not lines:
        raise MatrixParseError("empty")

    matrix = [parse_matrix_row(line, row_index) for row_index, line in enumerate(lines, start=1)]

    expected_columns = len(matrix[0])
    if expected_columns == 0:
        raise MatrixParseError("empty")

    for row_index, row in enumerate(matrix, start=1):
        if len(row) != expected_columns:
            raise MatrixParseError(
                "row_length",
                row=row_index,
                expected=expected_columns,
                actual=len(row),
            )

    return matrix


def normalized_matrix_lines(text):
    raw_lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    if len(raw_lines) == 1:
        semicolon_rows = split_single_line_rows(raw_lines[0])
        if semicolon_rows:
            return semicolon_rows
    return [trim_row_endings(line) for line in raw_lines]


def split_single_line_rows(line):
    parts = [trim_row_endings(part) for part in line.split(";") if part.strip()]
    if len(parts) <= 1:
        return []

    token_counts = [len(tokenize_matrix_row(part, include_semicolon=False)) for part in parts]
    if all(count > 1 for count in token_counts):
        return parts
    return []


def trim_row_endings(line):
    return line.strip().rstrip(";").strip()


def parse_matrix_row(line, row_index):
    tokens = tokenize_matrix_row(line)
    if not tokens:
        raise MatrixParseError("empty_row", row=row_index)

    row = []
    for column_index, token in enumerate(tokens, start=1):
        try:
            row.append(int(token))
        except ValueError as exc:
            raise MatrixParseError(
                "not_integer",
                row=row_index,
                column=column_index,
                value=token,
            ) from exc
    return row


def tokenize_matrix_row(line, include_semicolon=True):
    separators = r"[\s,;]+" if include_semicolon else r"[\s,]+"
    normalized = re.sub(r"[\[\]\(\)\{\}]", " ", line)
    return [token for token in re.split(separators, normalized.strip()) if token]


def parse_adjacency_matrix(text):
    try:
        matrix = parse_int_matrix(text)
    except MatrixParseError as exc:
        if exc.code == "row_length":
            raise MatrixParseError("square", row=exc.row, expected=exc.expected, actual=exc.actual) from exc
        raise
    if len(matrix) != len(matrix[0]):
        raise MatrixParseError("square", expected=len(matrix), actual=len(matrix[0]))
    for row_index, row in enumerate(matrix, start=1):
        for column_index, value in enumerate(row, start=1):
            if value < 0:
                raise MatrixParseError(
                    "negative_weight",
                    row=row_index,
                    column=column_index,
                    value=value,
                )
    return matrix


def parse_incidence_matrix(text):
    matrix = parse_int_matrix(text)
    for col in range(len(matrix[0])):
        values = [matrix[row][col] for row in range(len(matrix)) if matrix[row][col] != 0]
        if len(values) > 2:
            raise MatrixParseError(
                "incidence_column_size",
                column=col + 1,
                expected=2,
                actual=len(values),
            )
        if len(values) == 2 and abs(values[0]) != abs(values[1]):
            raise MatrixParseError(
                "incidence_weight_mismatch",
                column=col + 1,
                value=f"{values[0]} и {values[1]}",
            )
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
