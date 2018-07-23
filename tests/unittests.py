"""Unit tests of the branch and bound algorithm."""

import unittest

from test.test_graphs import SmallGraphs
from ktcut.branch_and_bound_algorithm import branch_and_bound_algorithm
from test.timetests import create_random_graph
from ktcut.minimum_isolating_cut import minimum_isolating_cut
from ktcut.ip_algorithm import ip_algorithm
from ktcut.lp_algorithm import lp_algorithm
from ktcut.contract_vertices import contract_vertices_several
from ktcut.persistence import test_persistence


class TestGraphs(unittest.TestCase):
    """Unit tests for the branch-and-bound algorithm."""

    def test_isolating_cut(self):
        test_graph = SmallGraphs()
        test_graph.set_test_graph(7)
        graph, terminals = test_graph.get_graph(), test_graph.get_terminals()
        cut_source, cut_weight = minimum_isolating_cut(graph, [1], [5, 6])
        self.assertEqual(cut_source, {1, 2, 3})
        self.assertEqual(cut_weight, 2.0)

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
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

    def test_graph_2(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(2)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 7.5)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

    def test_graph_3(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(3)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 24)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

    def test_graph_4(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(4)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

    def test_graph_5(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(5)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph,
                                                  terminals,
                                                  persistence='strong')
        self.assertEqual(cut_value, 110)
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 110)

    def test_graph_6(self):
        test_graphs = SmallGraphs()
        test_graphs.set_test_graph(6)
        graph, terminals = test_graphs.get_graph(), test_graphs.get_terminals()
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        cut_value = lp_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

    def test_graph_random(self):
        graph, terminals = create_random_graph('barabasi_albert', 100)
        partition_bb, cut_value_bb = branch_and_bound_algorithm(graph, terminals)
        partition_ip, cut_value_ip = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value_bb, cut_value_ip)
        self.assertEqual(partition_bb, partition_ip)
        self.assertTrue(test_persistence(graph, terminals, 'weak'))
        self.assertTrue(test_persistence(graph, terminals, 'strong'))

if __name__ == '__main__':
    unittest.main()