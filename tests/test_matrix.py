import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from matrix import (  # noqa: E402
    MatrixParseError,
    edges_from_adjacency_matrix,
    edges_from_incidence_matrix,
    format_matrix,
    incidence_matrix,
    parse_adjacency_matrix,
    parse_incidence_matrix,
    parse_int_matrix,
)


class MatrixParsingTests(unittest.TestCase):
    def test_accepts_commas_semicolons_tabs_and_brackets(self):
        text = "[0, 1; 2]\n(3\t4,5;)"
        self.assertEqual(parse_int_matrix(text), [[0, 1, 2], [3, 4, 5]])

    def test_accepts_single_line_semicolon_rows(self):
        text = "0 1 2; 1 0 3; 2 3 0"
        self.assertEqual(parse_int_matrix(text), [[0, 1, 2], [1, 0, 3], [2, 3, 0]])

    def test_semicolon_can_be_cell_separator(self):
        self.assertEqual(parse_int_matrix("0; 1; 2"), [[0, 1, 2]])

    def test_not_integer_error_has_position(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_int_matrix("0 1\n2 x")

        error = context.exception
        self.assertEqual(error.code, "not_integer")
        self.assertEqual(error.row, 2)
        self.assertEqual(error.column, 2)
        self.assertEqual(error.value, "x")

    def test_row_length_error_has_details(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_int_matrix("0 1 2\n1 0")

        error = context.exception
        self.assertEqual(error.code, "row_length")
        self.assertEqual(error.row, 2)
        self.assertEqual(error.expected, 3)
        self.assertEqual(error.actual, 2)

    def test_adjacency_matrix_must_be_square(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_adjacency_matrix("0 1 0\n1 0 2")

        error = context.exception
        self.assertEqual(error.code, "square")
        self.assertEqual(error.expected, 2)
        self.assertEqual(error.actual, 3)

    def test_adjacency_matrix_rejects_negative_weights(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_adjacency_matrix("0 -1\n0 0")

        error = context.exception
        self.assertEqual(error.code, "negative_weight")
        self.assertEqual(error.row, 1)
        self.assertEqual(error.column, 2)
        self.assertEqual(error.value, -1)

    def test_incidence_matrix_rejects_too_many_non_zero_values(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_incidence_matrix("1\n1\n1")

        error = context.exception
        self.assertEqual(error.code, "incidence_column_size")
        self.assertEqual(error.column, 1)
        self.assertEqual(error.actual, 3)

    def test_incidence_matrix_rejects_mismatched_weights(self):
        with self.assertRaises(MatrixParseError) as context:
            parse_incidence_matrix("2\n-3")

        error = context.exception
        self.assertEqual(error.code, "incidence_weight_mismatch")
        self.assertEqual(error.column, 1)
        self.assertEqual(error.value, "2 и -3")

    def test_matrix_edges_round_trip(self):
        matrix = parse_adjacency_matrix("0 1 0\n1 0 2\n0 0 0")
        edges = edges_from_adjacency_matrix(matrix)
        edge_data = [(edge.start_index, edge.end_index, edge.weight, int(edge.edge_type)) for edge in edges]

        self.assertEqual(edge_data, [(0, 1, 1, 1), (1, 2, 2, 0)])
        self.assertEqual(format_matrix(incidence_matrix(3, edges)), " 1   0\n 1   2\n 0  -2")

        incidence = parse_incidence_matrix("1 0\n1 2\n0 -2")
        incidence_edges = edges_from_incidence_matrix(incidence)
        incidence_edge_data = [
            (edge.start_index, edge.end_index, edge.weight, int(edge.edge_type))
            for edge in incidence_edges
        ]
        self.assertEqual(incidence_edge_data, [(0, 1, 1, 1), (1, 2, 2, 0)])


if __name__ == "__main__":
    unittest.main()
