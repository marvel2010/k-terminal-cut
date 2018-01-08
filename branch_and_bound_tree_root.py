"""Derives key properties at the Branch and Bound tree root."""
from combined_vertices import contract_vertices_several
from minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeRoot:
    """Preprocessing for multi-terminal cut"""

    def __init__(self, graph, terminals, terminals_by_vertex):
        self.graph = graph
        self.terminals = terminals
        if terminals_by_vertex is not None:
            self.terminals_by_vertex = terminals_by_vertex
        else:
            self.terminals_by_vertex = {node: terminals for node in graph.nodes()}

    def combine_terminal_sets(self, terminal_sets):
        """A set of nodes pre-assigned to a particular terminal."""
        for terminal in self.terminals:
            self.graph = contract_vertices_several(self.graph, terminal, terminal_sets[terminal]-{terminal})

    def initial_isolating_cuts(self):
        """The initial isolating cuts."""
        for terminal in self.terminals:
            source_set, weight = minimum_isolating_cut(self.graph,
                                                       source_nodes={terminal},
                                                       sink_nodes=set(self.terminals)-{terminal})
            self.graph = contract_vertices_several(self.graph, terminal, source_set-{terminal})

    def get_graph(self):
        return self.graph

    def get_terminals(self):
        return self.terminals

    def get_terminals_by_vertex(self):
        return self.terminals_by_vertex