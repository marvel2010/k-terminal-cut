"""Defines a Root in the Branch and Bound Tree for Isolation Branching."""
from copy import deepcopy
from ktcut.contract_vertices import contract_vertices
from ktcut.minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeRoot:
    """Pre-processing for k-terminal cut problem."""

    def __init__(self, graph, terminals):
        self._graph = deepcopy(graph)
        self._terminals = terminals

    def initial_isolating_cuts(self):
        """Performs the initial isolating cuts.

        The initial isolating cuts are the k minimum cuts
            that separate one terminal from the rest.
        """
        for terminal in self._terminals:
            source_set, weight = minimum_isolating_cut(
                self._graph,
                source_vertices={terminal},
                sink_vertices=set(self._terminals) - {terminal},
            )
            self._graph = contract_vertices(
                self._graph, terminal, source_set - {terminal}
            )

    def get_graph(self):
        """self.graph"""
        return self._graph
