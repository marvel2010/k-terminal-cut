"""Defines a Node in the Branch and Bound Tree"""

from copy import deepcopy

from ktcut.contract_vertices import contract_vertex
from ktcut.contract_vertices import contract_vertices_several
from ktcut.minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeNode:
    """Node in the branch-and-bound tree for multi-terminal cut.

    Attributes:
        input_graph: a graph in which all previous isolating cuts
            have been merged to terminals
        input_terminals: terminals in the graph
        new_vertex: the lonely vertex to add to a terminal
            from the parent node
        new_vertex_terminal: the terminal to add the lonely vertex
            from the parent node
    """

    def __init__(self,
                 input_graph,
                 input_terminals,
                 new_vertex=None,
                 new_vertex_terminal=None,
                 depth=0):

        # deep copy at this level is important
        self.graph = deepcopy(input_graph)
        self.terminals = input_terminals
        self.new_vertex = new_vertex
        self.new_vertex_terminal = new_vertex_terminal
        self.depth = depth

        self.children = []

        # run expansions
        if self.new_vertex is not None and self.new_vertex_terminal is not None:
            self._source_set_add_vertex()
            self._source_set_isolating_cut()

        self.lower_bound = self._sum_of_source_adjacent_edges()

    def _source_set_add_vertex(self):
        # copy required because we try adding the same vertex
        # to several source sets
        self.graph = contract_vertex(self.graph, self.new_vertex_terminal, self.new_vertex)

    def _source_set_isolating_cut(self):
        source_set, weight = minimum_isolating_cut(self.graph,
                                                   source_nodes={self.new_vertex_terminal},
                                                   sink_nodes=set(self.terminals)-{self.new_vertex_terminal})
        self.graph = contract_vertices_several(self.graph,
                                               self.new_vertex_terminal,
                                               source_set-{self.new_vertex_terminal}
        )

    def _add_child(self, new_vertex, new_vertex_terminal):
        """Creates a new child of this tree node.

        Creates a new child of this tree node by adding new_node to
            the source set of new_vertex_terminal.

        Params:
            new_node: the node to be added (previously lonely)
            new_source_set: the set this new node will be added to
        """
        child = BranchAndBoundTreeNode(self.graph,
                                       self.terminals,
                                       new_vertex,
                                       new_vertex_terminal,
                                       depth=self.depth+1)
        assert child.lower_bound >= self.lower_bound, ' created bad child '
        self.children.append(child)

    def _sum_of_source_adjacent_edges(self):
        """
        Calculates half the sum of the capacities of edges adjacent to terminals.

        Args:
            (None)

        Returns:
            capacity_sum
        """
        capacity_sum = 0
        for terminal in self.terminals:
            neighbors = self.graph[terminal]
            for neighbor in neighbors:
                capacity_sum += self.graph[terminal][neighbor]['capacity']
        return capacity_sum / 2

    def construct_children_nodes(self, lonely_vertex, allowed_terminals):
        """Runs _add_child for each possible source set."""
        assert not self.children, 'children already created'
        for terminal in allowed_terminals:
            self._add_child(new_vertex=lonely_vertex, new_vertex_terminal=terminal)

    def find_lonely_vertices(self):
        """Finds the vertices in the graph which are lonely."""
        lonely_vertices = set(self.graph.nodes()) - set(self.terminals)
        return lonely_vertices