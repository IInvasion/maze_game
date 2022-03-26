"""Tests for Kruskal algorithm."""

import unittest

from . import data
from .. import kruskal


class TestKruskal(unittest.TestCase):
    """Tests for Kruskal algorithm."""

    def case(self, edges, correct, debug=False):
        """Test case."""
        result = kruskal.build_tree(edges, debug=debug)
        self.assertEqual(result, correct)

    def test_2x2(self):
        """Test some 2x2 maze cases."""
        correct_1 = [
            ((1, 0), (1, 1)), ((0, 0), (0, 1)), ((0, 1), (1, 1))
        ]
        self.case(data.EDGES_1, correct_1)

        correct_2 = [
            ((1, 0), (1, 1)), ((0, 0), (1, 0)), ((0, 0), (0, 1))
        ]
        self.case(data.EDGES_2, correct_2)
