"""Derives key properties at the Branch and Bound tree root."""
from copy import deepcopy

from ktcut.contract_vertices import contract_vertices_several
from ktcut.minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeRoot:
    """Pre-processing for k-terminal cut problem."""

    def __init__(self, graph, terminals):
        self._graph = deepcopy(graph)
        self._terminals = terminals

    def initial_isolating_cuts(self):
        """
        Performs the initial isolating cuts.

        The initial isolating cuts are the k minimum cuts
            that separate one terminal from the rest.
        """
        for terminal in self._terminals:
            source_set, weight = minimum_isolating_cut(
                self._graph,
                source_nodes={terminal},
                sink_nodes=set(self._terminals) - {terminal},
            )
            self._graph = contract_vertices_several(
                self._graph, terminal, source_set - {terminal}
            )

    def get_graph(self):
        """self.graph"""
        return self._graph
