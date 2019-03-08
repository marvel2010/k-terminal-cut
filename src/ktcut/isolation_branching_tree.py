"""Defines the overall Branch and Bound Tree for Isolation Branching."""
import networkx as nx
import numpy as np
from typing import List
from ktcut.branch_and_bound_node import IsolationBranchingNode
from ktcut.branch_and_bound_root import IsolationBranchingRoot
import time


class IsolationBranchingTree:
    """Tree for isolation branching for k-terminal cut.

    Attributes:
        terminals: the set of terminals
        _root_node: the root node of the branch and bound tree
        _unexplored_nodes: a list of the unexplored nodes in the tree
        _all_nodes: a list of all nodes in the tree
        _done: if the algorithm terminated
        _active_node: the node which is currently being considered
        _start_time: when the branch and bound tree was initialized
    """

    def __init__(self, graph, terminals, terminals_by_vertex):
        self._root_node = IsolationBranchingRoot(graph, terminals)
        self._terminals = terminals
        self._terminals_by_vertex = terminals_by_vertex
        self._done: bool = False
        self._unexplored_nodes: List[IsolationBranchingNode] = None
        self._all_nodes: List[IsolationBranchingNode] = None
        self._active_node: IsolationBranchingNode = None
        self._nodes_explored_count: int = 0
        self._start_time = time.time()

    @property
    def best_lower_bound(self):
        """The lowest lower bound among all nodes."""
        if self._unexplored_nodes:
            return min(node.lower_bound for node in self._unexplored_nodes)
        else:
            return 0.0

    @property
    def best_upper_bound(self):
        """The lowest upper bound among all nodes."""
        if self._all_nodes:
            return min(node.upper_bound for node in self._all_nodes)
        else:
            return np.inf

    @property
    def unexplored_nodes_count(self):
        return len(self._unexplored_nodes)

    @property
    def total_nodes_count(self):
        return len(self._all_nodes)

    def _pop_node_with_best_lower_bound(self) -> IsolationBranchingNode:
        self._unexplored_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        # NB: pop() will return the last element of the list
        return self._unexplored_nodes.pop()

    def _pop_node_with_maximum_depth(self) -> IsolationBranchingNode:
        self._unexplored_nodes.sort(key=lambda x: (x.depth, -x.lower_bound))
        # NB: pop() will return the last element of the list
        return self._unexplored_nodes.pop()

    def _node_with_best_upper_bound(self) -> IsolationBranchingNode:
        self._all_nodes.sort(key=lambda x: x.upper_bound)
        return self._all_nodes[0]

    def _choose_unassigned_vertex_highest_degree(self):
        degrees = dict(nx.degree(self._active_node.graph, weight="capacity"))
        degrees_restricted = {
            node: node_degree
            for node, node_degree in degrees.items()
            if node in self._active_node.unassigned_vertices
        }
        return max(degrees_restricted, key=degrees_restricted.get)

    def _step(self):
        """One step of the branch-and-bound algorithm.

            (1) Select a Node
            (2) Select a Vertex
            (3) Branch
        """
        if self.best_lower_bound < self.best_upper_bound:

            # Select a Node
            self._active_node = self._pop_node_with_best_lower_bound()

            # Select a Vertex
            unassigned_vertex_chosen = self._choose_unassigned_vertex_highest_degree()

            # Branch
            self._active_node.construct_children_nodes(
                unassigned_vertex_chosen,
                self._terminals_by_vertex[unassigned_vertex_chosen],
            )

            # NB: we do not need to worry about duplicate nodes
            # the nodes are constructed by forcing an assignment of
            # vertices to terminals. Thus, the resulting partitions
            # can never be identical
            self._unexplored_nodes += self._active_node.children
            self._all_nodes += self._active_node.children

        else:
            # if there are no unassigned vertices, we are at a leaf node
            self._done = True

    def solve(self, reporting=False):
        """Solves k-terminal cut using isolation branching.

        Returns:
            source_sets: the nodes that remain connected to each terminal
            cut_value: the cost of the multi-terminal cut
        """
        self._root_node.initial_isolating_cuts()
        graph = self._root_node.get_graph()
        first_node = IsolationBranchingNode(graph, self._terminals, None, None)
        self._all_nodes = [first_node]
        self._unexplored_nodes = [first_node]

        while not self._done:
            self._step()
            if reporting:
                print(self.report)

        # done
        self._active_node = self._node_with_best_upper_bound()
        final_node_source_sets = {}
        for terminal in self._terminals:
            if "combined" in self._active_node.graph.node[terminal]:
                final_node_source_sets[terminal] = self._active_node.graph.node[
                    terminal
                ]["combined"] | {terminal}
            else:
                final_node_source_sets[terminal] = {terminal}

        return final_node_source_sets, round(self._active_node.lower_bound, 8)

    @property
    def report(self):
        return {
            "Source Set Sizes": {
                terminal: len(self._active_node.graph.nodes[terminal]["combined"])
                for terminal in self._terminals
            },
            "Node Depth": self._active_node.depth,
            "Node Lower Bound": self._active_node.lower_bound,
            "Node Upper Bound": self._active_node.upper_bound,
            "Total Unassigned Vertices": len(
                set(self._active_node.graph.nodes()) - set(self._terminals)
            ),
            "Best Lower Bound": self.best_lower_bound,
            "Best Upper Bound": self.best_upper_bound,
            "Nodes Unexplored": self.unexplored_nodes_count,
            "Nodes Total": self.total_nodes_count,
            "Time Elapsed": time.time() - self._start_time
        }
