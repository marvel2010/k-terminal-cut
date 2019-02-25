"""Defines the overall Branch and Bound Tree for Isolation Branching."""
import networkx as nx
import numpy as np
from ktcut.branch_and_bound_node import IsolationBranchingNode
from ktcut.branch_and_bound_root import IsolationBranchingRoot
import time


class IsolationBranchingTree:
    """Tree for isolation branching for k-terminal cut.

    Attributes:
        terminals: the set of terminals
        _root_node: the root node of the branch and bound tree
        _all_nodes: a list of all nodes in the tree
        _best_lower_bound: the best lower bound on the objective so far
        _best_upper_bound: the best feasible solution so far
        _done: if the algorithm terminated
        _active_node: the node which is currently being considered
        _nodes_explored_count: total number of nodes explored
        _start_time: when the branch and bound tree was initialized
    """

    def __init__(self, graph, terminals, terminals_by_vertex):
        self._root_node = IsolationBranchingRoot(graph, terminals)
        self._terminals = terminals
        self._terminals_by_vertex = terminals_by_vertex
        self._best_lower_bound = 0.0
        self._best_upper_bound = np.inf
        self._done = False
        self._all_nodes = None
        self._active_node: IsolationBranchingNode = None
        self._nodes_explored_count: int = 0
        self._start_time = time.time()

    def _step(self):
        """One step of the branch-and-bound algorithm.

            (1) Picks the node with the lowest lower bound
            (2) Finds an unassigned vertex
            (3) Creates new tree nodes
        """

        self._all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        self._active_node = self._all_nodes.pop()

        if self._active_node.unassigned_vertices:
            # if there are still unassigned vertices, we branch
            unassigned_vertex_chosen = self._choose_unassigned_vertex_highest_degree()

            # choose the set of possible terminals for this node
            self._active_node.construct_children_nodes(
                unassigned_vertex_chosen,
                self._terminals_by_vertex[unassigned_vertex_chosen],
            )

            # note: we do not need to worry about duplicate nodes
            # the nodes are constructed by forcing an assignment of
            # vertices to terminals. Thus, the resulting partitions
            # can never be identical
            self._all_nodes += self._active_node.children

            assert (
                self._active_node.lower_bound >= self._best_lower_bound
            ), "lower bound issue"

            if self._active_node.lower_bound > self._best_lower_bound:
                self._best_lower_bound = self._active_node.lower_bound
            if self._active_node.upper_bound < self._best_upper_bound:
                self._best_upper_bound = self._active_node.upper_bound
        else:
            # if there are no unassigned vertices, we are at a leaf node
            self._done = True

    def _choose_unassigned_vertex_highest_degree(self):
        degrees = dict(nx.degree(self._active_node.graph, weight="capacity"))
        degrees_restricted = {
            node: node_degree
            for node, node_degree in degrees.items()
            if node in self._active_node.unassigned_vertices
        }
        return max(degrees_restricted, key=degrees_restricted.get)

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
            "Best Lower Bound": self._best_lower_bound,
            "Best Upper Bound": self._best_upper_bound,
            "Nodes Explored": self._nodes_explored_count,
            "Time Elapsed": time.time() - self._start_time
        }

    def solve(self, reporting=False):
        """Solves k-terminal cut using isolation branching.

        Returns:
            source_sets: the nodes that remain connected to each terminal
            cut_value: the cost of the multi-terminal cut
        """
        self._root_node.initial_isolating_cuts()
        graph = self._root_node.get_graph()
        self._all_nodes = [IsolationBranchingNode(graph, self._terminals, None, None)]

        while not self._done:
            self._step()
            self._nodes_explored_count += 1
            if reporting:
                print(self.report)

        final_node_source_sets = {}
        for terminal in self._terminals:
            if "combined" in self._active_node.graph.node[terminal]:
                final_node_source_sets[terminal] = self._active_node.graph.node[
                    terminal
                ]["combined"] | {terminal}
            else:
                final_node_source_sets[terminal] = {terminal}

        return final_node_source_sets, round(self._active_node.lower_bound, 8)
