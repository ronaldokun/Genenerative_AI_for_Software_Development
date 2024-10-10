import unittest
from collections import deque
from graph import Graph

class TestGraph(unittest.TestCase):

    def setUp(self):
        self.graph = Graph(directed=False)
        self.graph.add_vertex('A')
        self.graph.add_vertex('B')
        self.graph.add_vertex('C')
        self.graph.add_edge('A', 'B')
        self.graph.add_edge('A', 'C')

    def test_add_vertex(self):
        self.graph.add_vertex('D')
        self.assertIn('D', self.graph.graph)

    def test_add_edge(self):
        self.graph.add_edge('B', 'C')
        self.assertIn('C', self.graph.get_adjacent_vertices('B'))

    def test_remove_edge(self):
        self.graph.remove_edge('A', 'B')
        self.assertNotIn('B', self.graph.get_adjacent_vertices('A'))
        self.assertNotIn('A', self.graph.get_adjacent_vertices('B'))

    def test_remove_vertex(self):
        self.graph.remove_vertex('A')
        self.assertNotIn('A', self.graph.graph)
        self.assertNotIn('A', self.graph.get_adjacent_vertices('B'))
        self.assertNotIn('A', self.graph.get_adjacent_vertices('C'))

    def test_bfs(self):
        result = self.graph.bfs('A')
        self.assertEqual(result, ['A', 'B', 'C'])

    def test_dfs(self):
        result = self.graph.dfs('A')
        self.assertEqual(result, ['A', 'C', 'B'])

    def test_add_edge_non_existent_vertex(self):
        with self.assertRaises(KeyError):
            self.graph.add_edge('A', 'D')

    def test_remove_edge_non_existent(self):
        with self.assertRaises(ValueError):
            self.graph.remove_edge('A', 'D')

    def test_remove_vertex_non_existent(self):
        with self.assertRaises(KeyError):
            self.graph.remove_vertex('D')

    def test_empty_graph_operations(self):
        empty_graph = Graph()
        with self.assertRaises(ValueError):
            empty_graph.remove_edge('A', 'B')
        with self.assertRaises(ValueError):
            empty_graph.remove_vertex('A')

if __name__ == '__main__':
    unittest.main()