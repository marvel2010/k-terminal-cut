"""Defines a Node in the Branch and Bound Tree"""

from itertools import chain
from copy import deepcopy
from minimum_isolating_cut import minimum_isolating_cut


class BranchAndBoundTreeNode:
    """Node in the branch-and-bound tree for multi-terminal cut.

    Attributes:
        parent_node
        children
        graph
        source_sets
        iso_cut_weights
    """

    def __init__(self,
                 parent_node=None,
                 new_vertex=None,
                 new_vertex_source_set=None,
                 is_root=False,
                 in_graph=None,
                 root_terminals=None,
                 is_intermediate=False,
                 int_source_sets=None):

        if is_root:
            # assertions
            assert parent_node is None
            assert new_vertex is None
            assert new_vertex_source_set is None
            assert in_graph is not None
            assert root_terminals is not None
            assert int_source_sets is None

            # init variables
            self.parent_node = None
            self.children = []
            self.graph = in_graph
            self.source_sets = {}
            self.iso_cut_weights = {}

            for terminal in root_terminals:
                self.source_sets[terminal] = set()
                self.source_sets[terminal].add(terminal)

            # run expansion
            for terminal in root_terminals:
                self._expand_source_set(terminal)

            # run checks
            for terminal in self.source_sets:
                # check that every terminal set contains its terminal
                assert terminal in self.source_sets[terminal], ' init without contained terminals '
                for terminal2 in self.source_sets:
                    if terminal != terminal2:
                        # check that pairs of terminal sets do not contain overlap
                        assert (len(self.source_sets[terminal]
                                    & self.source_sets[terminal2]) == 0), ' init with overlap '

        elif is_intermediate:
            # assertions
            assert parent_node is None
            assert new_vertex is None
            assert new_vertex_source_set is None
            assert in_graph is not None
            assert root_terminals is not None
            assert int_source_sets is not None

            # init variables
            self.parent_node = None
            self.children = []
            self.graph = in_graph
            self.source_sets = int_source_sets

            # run expansion
            self.iso_cut_weights = {}
            for terminal in root_terminals:
                self._expand_source_set(terminal)

        else:
            # assertions
            assert parent_node is not None
            assert new_vertex is not None
            assert new_vertex_source_set is not None
            assert in_graph is None
            assert root_terminals is None
            assert int_source_sets is None

            # init variables
            self.parent_node = parent_node
            self.children = []
            self.graph = parent_node.graph
            self.source_sets = deepcopy(parent_node.source_sets)
            self.iso_cut_weights = deepcopy(parent_node.iso_cut_weights)

            # run expansion
            self.source_sets[new_vertex_source_set].add(new_vertex)
            self._expand_source_set(new_vertex_source_set)

            # run checks
            assert (self.source_sets[new_vertex_source_set]
                    > self.parent_node.source_sets[new_vertex_source_set]), ' subset problem '

        self.lower_bound = self.calculate_lower_bound()

    def _add_child(self, new_node, new_source_set):
        """Creates a new child of this tree node.

        Creates a new child of this tree node by adding new_node to
            new_source_set.

        Params:
            new_node: the node to be added (previously lonely)
            new_source_set: the set this new node will be added to
        """
        child = BranchAndBoundTreeNode(self, new_node, new_source_set)
        assert child.lower_bound >= self.lower_bound, ' created bad child '
        self.children.append(child)

    def _expand_source_set(self, target_source_set):
        self.source_sets[target_source_set], self.iso_cut_weights[target_source_set] = \
            minimum_isolating_cut(self.graph,
                                  source_nodes=self.source_sets[target_source_set],
                                  sink_nodes=set(chain.from_iterable([self.source_sets[index]
                                                                      for index in self.source_sets.keys()
                                                                      if index != target_source_set])
                                                )
                                 )

    def construct_children_nodes(self, lonely_vertex, allowed_terminals):
        """Runs _add_child for each possible source set."""
        assert len(self.children) == 0, 'children already created'
        for terminal in allowed_terminals:
            self._add_child(new_node=lonely_vertex, new_source_set=terminal)

    def find_lonely_vertices(self):
        """Finds the nodes in the graph which are lonely"""
        lonely_vertices = set(self.graph.nodes()) - set(chain.from_iterable(self.source_sets.values()))
        return lonely_vertices

    def calculate_lower_bound(self):
        """Calculates the lower bound on the objective function at this node."""
        return sum(list(self.iso_cut_weights.values())) / 2
