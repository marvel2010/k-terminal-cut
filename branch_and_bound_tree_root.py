"""Derives key properties at the Branch and Bound tree root."""
from contract_vertices import contract_vertices_several
from minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeRoot:
    """Preprocessing for multi-terminal cut"""

    def __init__(self, graph, terminals):
        self.graph = graph
        self.terminals = terminals

    def initial_isolating_cuts(self):
        """The initial isolating cuts."""
        for terminal in self.terminals:
            source_set, weight = minimum_isolating_cut(self.graph,
                                                       source_nodes={terminal},
                                                       sink_nodes=set(self.terminals)-{terminal})
            self.graph = contract_vertices_several(self.graph, terminal, source_set-{terminal})

    def get_graph(self):
        """self.graph"""
        return self.graph

    def get_terminals(self):
        """self.terminals"""
        return self.terminals