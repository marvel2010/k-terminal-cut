"""Defines small graphs used for test cases."""

import itertools
import networkx as nx


class SmallGraphs():

    def __init__(self):
        self.graph = None
        self.terminals = None

    def _set_test_graph_1(self):
        """Graph with LP 8, IP 8"""
        self.graph = nx.Graph()
        self.graph.add_nodes_from([i for i in range(1, 9)])
        self.graph.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)], capacity=2)
        self.graph.add_edges_from([(1, 5), (2, 6), (3, 7), (4, 8)], capacity=3)
        self.terminals = range(1, 5)

    def _set_test_graph_2(self):
        """graph with LP 7.5, IP 8"""
        self.graph = nx.Graph()
        self.graph.add_nodes_from([1, 2, 3, 12, 13, 23])
        self.graph.add_edges_from([(1, 12), (1, 13), (2, 12), (2, 23), (3, 13), (3, 23)], capacity=2)
        self.graph.add_edges_from([(12, 13), (13, 23), (12, 23)], capacity=1)
        self.terminals = range(1, 4)

    def _set_test_graph_3(self):
        """graph with LP 24, IP 26"""
        self.graph = nx.Graph()
        self.terminals = range(1, 5)
        self.graph.add_nodes_from([1, 2, 3, 4, 12, 13, 14, 23, 24, 34])
        self.graph.add_edges_from([(1, 12), (1, 13), (1, 14),
                                   (2, 12), (2, 23), (2, 24),
                                   (3, 13), (3, 23), (3, 34),
                                   (4, 14), (4, 24), (4, 34)],
                                  capacity=3)
        self.graph.add_edges_from([(12, 13), (12, 14), (12, 23), (12, 24),
                                   (13, 14), (13, 23), (13, 34),
                                   (14, 24), (14, 34),
                                   (23, 24), (23, 34),
                                   (24, 34)], capacity=1)

    def _set_test_graph_4(self):
        """graph with LP 26, IP 27"""
        self.graph = nx.Graph()
        self.terminals = range(1, 5)
        self.graph.add_nodes_from([1, 2, 3, 4, 123, 124, 134, 234])
        self.graph.add_edges_from([(1, 123), (1, 124), (1, 134),
                                   (2, 123), (2, 124), (2, 234),
                                   (3, 123), (3, 134), (3, 234),
                                   (4, 124), (4, 134), (4, 234)],
                                  capacity=3)
        self.graph.add_edges_from([(123, 124), (123, 134), (123, 234),
                                   (124, 134), (124, 234),
                                   (134, 234)],
                                  capacity=1)

    def _set_test_graph_5(self):
        """graph with LP 110, IP 110"""
        self.graph = nx.Graph()
        self.terminals = range(1, 6)
        subset_sizes = 3
        agreement = 1
        self.graph.add_nodes_from(self.terminals)
        self.graph.add_nodes_from(itertools.combinations(self.terminals, subset_sizes))
        self.graph.add_edges_from([(a, b)
                                   for a in self.terminals
                                   for b in itertools.combinations(self.terminals, subset_sizes)
                                   if a in set(b)], capacity=5)
        self.graph.add_edges_from([(a, b)
                                   for a in itertools.combinations(self.terminals, subset_sizes)
                                   for b in itertools.combinations(self.terminals, subset_sizes)
                                   if len(set(a) & set(b)) == agreement], capacity=1)

    def _set_test_graph_6(self):
        """
        gadget used to prove NP-completeness in original paper
        graph with LP 27, IP 27
        """
        self.graph = nx.Graph()
        self.terminals = [1, 5, 9]
        self.graph.add_nodes_from(range(1, 10))
        self.graph.add_edges_from([(2, 3), (2, 8), (3, 6), (4, 6), (4, 7), (7, 8)], capacity=1)
        self.graph.add_edges_from([(1, 2), (1, 3), (1, 4), (1, 7), (2, 5), (3, 9),
                                   (4, 5), (5, 6), (5, 8), (6, 9), (7, 9), (8, 9)], capacity=4)

    def _set_test_graph_7(self):
        """
        the minimum isolating cut should have size 2 and should have a source set of size 3.
        """
        self.graph = nx.Graph()
        self.terminals = [1, 5, 6]
        self.graph.add_nodes_from(range(1, 7))
        self.graph.add_edges_from([(1, 2), (3, 4), (4, 5), (4, 6)], capacity=2)
        self.graph.add_edges_from([(2, 3)], capacity=3)

    def set_test_graph(self, index):
        if index == 1:
            self._set_test_graph_1()
        elif index == 2:
            self._set_test_graph_2()
        elif index == 3:
            self._set_test_graph_3()
        elif index == 4:
            self._set_test_graph_4()
        elif index == 5:
            self._set_test_graph_5()
        elif index == 6:
            self._set_test_graph_6()
        elif index == 7:
            self._set_test_graph_7()
        else:
            raise ValueError

    def get_terminals(self):
        return self.terminals

    def get_graph(self):
        return self.graph