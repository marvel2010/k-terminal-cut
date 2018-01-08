"""Defines a Node in the Branch and Bound Tree"""

from itertools import chain
from minimum_isolating_cut import minimum_isolating_cut
from combined_vertices import combined_vertices
from combined_vertices import combined_vertices_several


class BranchAndBoundTreeNode:
    """Node in the branch-and-bound tree for multi-terminal cut.

    Attributes:
        input_graph: a graph in which all previous isolating cuts have been merged
        input_terminals: TODO
        new_vertex: TODO
        new_vertex_terminal: TODO
    """

    def __init__(self,
                 input_graph=None,
                 input_terminals=None,
                 new_vertex=None,
                 new_vertex_terminal=None):

        self.graph = input_graph
        self.terminals = input_terminals
        self.new_vertex = new_vertex
        self.new_vertex_terminal = new_vertex_terminal

        self.children = []

        # run expansions
        if new_vertex is not None and new_vertex_terminal is not None:
            self._source_set_add_vertex()
            self._source_set_isolating_cut()

        self.lower_bound = self._calculate_lower_bound()

    def _source_set_add_vertex(self):
        self.graph = combined_vertices(self.graph, self.new_vertex_terminal, self.new_vertex)

    def _source_set_isolating_cut(self):
        source_set, weight = minimum_isolating_cut(self.graph,
                                                   source_nodes={self.new_vertex_terminal},
                                                   sink_nodes=set(self.terminals)-{self.new_vertex_terminal})
        self.graph = combined_vertices_several(self.graph, self.new_vertex_terminal, source_set-{self.new_vertex_terminal})

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
                                       new_vertex_terminal)
        assert child.lower_bound >= self.lower_bound, ' created bad child '
        self.children.append(child)

    def _calculate_lower_bound(self):
        """Calculates the lower bound on the objective function at this node."""
        sm = 0
        for terminal in self.terminals:
            neighbors = self.graph[terminal]
            for neighbor in neighbors:
                sm += self.graph[terminal][neighbor]['capacity']
        return sm / 2

    def construct_children_nodes(self, lonely_vertex, allowed_terminals):
        """Runs _add_child for each possible source set."""
        assert len(self.children) == 0, 'children already created'
        for terminal in allowed_terminals:
            self._add_child(new_vertex=lonely_vertex, new_vertex_terminal=terminal)

    def find_lonely_vertices(self):
        """Finds the nodes in the graph which are lonely."""
        lonely_vertices = set(self.graph.nodes()) - set(self.terminals)
        return lonely_vertices