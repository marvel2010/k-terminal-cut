"""Unit tests of the branch and bound algorithm."""

from test_graphs import SmallGraphs
from timetests import create_random_graph
import unittest
from branch_and_bound_algorithm import branch_and_bound_algorithm
from ip_algorithm import ip_algorithm
from lp_algorithm import lp_algorithm
from combined_vertices import contract_vertices_several
from persistence import test_weak_persistence
from persistence import test_strong_persistence


class TestGraphs(unittest.TestCase):
    """Unit tests for the branch-and-bound algorithm."""

    def test_combined_vertices(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(1)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        graph = contract_vertices_several(graph, 1, {5, 7, 8})
        self.assertEqual(graph[1][6]['capacity'], 4)

    def test_graph_1(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(1)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

    def test_graph_2(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(2)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 7.5)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

    def test_graph_3(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(3)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 24)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

    def test_graph_4(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(4)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

    def test_graph_5(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(5)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        terminals_by_vertex, _ = lp_algorithm(graph,
                                              terminals,
                                              persistence_sets=True)
        _, cut_value = branch_and_bound_algorithm(graph,
                                                  terminals,
                                                  terminals_by_vertex=terminals_by_vertex)
        self.assertEqual(cut_value, 110)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 110)

    def test_graph_6(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(6)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

    def test_graph_random(self):
        graph, terminals = create_random_graph('barabasi_albert', 100)
        _, cut_value_bb = branch_and_bound_algorithm(graph, terminals)
        _, cut_value_ip = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value_bb, cut_value_ip)
        self.assertTrue(test_weak_persistence(graph, terminals))
        self.assertTrue(test_strong_persistence(graph, terminals))

if __name__ == '__main__':
    unittest.main()
