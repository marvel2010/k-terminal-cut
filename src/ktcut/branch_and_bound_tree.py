"""Defines the overall branch and bound tree."""

import networkx as nx

from ktcut.branch_and_bound_tree_node import BranchAndBoundTreeNode
from ktcut.branch_and_bound_tree_root import BranchAndBoundTreeRoot


class BranchAndBoundTree:
    """Tree for multi-terminal cut

    Attributes:
        terminals: the set of terminals
        root_node: the root node of the branch and bound tree
        all_nodes: a list of all nodes in the tree
        global_lower_bound: the best lower bound on the objective so far
        done: if the algorithm terminated
        node_with_lowest_bound: the node which is currently being considered
        lonely_vertices: the set of vertices lonely at the current node
    """

    def __init__(self, graph, terminals, terminals_by_vertex):
        self._root_node = BranchAndBoundTreeRoot(graph, terminals)
        self._terminals = terminals
        self._terminals_by_vertex = terminals_by_vertex
        self._global_lower_bound = 0.0
        self._done = False
        self._all_nodes = None
        self._active_node = None
        self._active_node_lonely_vertices = None
        self.nodes_explored_count = 0

    def _step(self):
        """One step of the branch-and-bound algorithm.

        (1) Picks the node with the lowest lower bound
        (2) Finds a lonely vertex
        (3) Creates new tree nodes
        """

        self._all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        self._active_node = self._all_nodes.pop()
        self._active_node_lonely_vertices = \
            self._active_node.find_lonely_vertices()

        if not self._active_node_lonely_vertices:
            self._done = True
            return

        else:
            # if there are still lonely vertices
            lonely_vertex_chosen = self._choose_lonely_node_highest_degree()

            # choose the set of possible terminals for this node
            self._active_node.construct_children_nodes(lonely_vertex_chosen,
                                                       self._terminals_by_vertex[lonely_vertex_chosen])

            # note: we do not need to worry about duplicate nodes
            # the nodes are constructed by forcing an assignment of
            # vertices to terminals. Thus, the resulting partitions
            # can never be identical
            self._all_nodes += self._active_node.children

            assert (self._active_node.lower_bound
                    >= self._global_lower_bound), 'lower bound issue'

            self._global_lower_bound = self._active_node.lower_bound
            return

    def _choose_lonely_node_highest_degree(self):
        degrees = dict(nx.degree(self._active_node.graph, weight='capacity'))
        degrees_restricted = {node: node_degree
                              for node, node_degree in degrees.items()
                              if node in self._active_node_lonely_vertices}
        return max(degrees_restricted, key=degrees_restricted.get)

    def print_source_sets(self):
        for terminal in self._terminals:
            print("Source Set for Terminal %s" % terminal,
                  self._active_node.graph.nodes[terminal])
        print()

    def print_source_set_sizes(self):
        for terminal in self._terminals:
            print("Source Set Size for Terminal %s" % terminal,
                  len(self._active_node.graph.nodes[terminal]['combined']))
        print("Node Depth", self._active_node.depth)
        print("Node Bound", self._active_node._sum_of_source_adjacent_edges())
        print("Total Accounted Vertices",
              sum(len(self._active_node.graph.nodes[terminal]['combined'])
                  for terminal in self._terminals))
        print("Total Unaccounted Vertices",
              len(set(self._active_node.graph.nodes()) - set(self._terminals)))
        print()

    def solve(self, reporting=False):
        """Solves the multi-terminal cut using the branch-and-bound algorithm.

        Returns:
            source_sets: the nodes that remain connected to each terminal
            cut_value: the cost of the multi-terminal cut
        """
        self._root_node.initial_isolating_cuts()
        graph = self._root_node.get_graph()
        self._all_nodes = [BranchAndBoundTreeNode(graph,
                                                  self._terminals,
                                                  None,
                                                  None)
        ]

        while not self._done:
            self._step()
            if reporting:
                self.print_source_set_sizes()
            self.nodes_explored_count += 1

        final_node_source_sets = {}
        for terminal in self._terminals:
            if 'combined' in self._active_node.graph.node[terminal]:
                final_node_source_sets[terminal] = (self._active_node.graph.node[terminal]['combined']
                                                    | {terminal})
            else:
                final_node_source_sets[terminal] = {terminal}

        return final_node_source_sets, round(self._active_node.lower_bound, 8)
