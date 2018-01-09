"""Defines the overall branch and bound tree."""

import numpy as np
import networkx as nx
from branch_and_bound_tree_node import BranchAndBoundTreeNode
from branch_and_bound_tree_root import BranchAndBoundTreeRoot


class BranchAndBoundTree:
    """Tree for multi-terminal cut

    Attributes:
        all_nodes
        global_lower_bound
        done
        node_with_lowest_bound
        lonely_nodes
    """

    def __init__(self, graph, terminals, terminals_by_vertex):
        root_node = BranchAndBoundTreeRoot(graph, terminals)
        root_node.initial_isolating_cuts()
        graph = root_node.get_graph()
        self.terminals = root_node.get_terminals()

        self.terminals_by_vertex = terminals_by_vertex
        self.all_nodes = [BranchAndBoundTreeNode(graph, terminals, None, None)]
        self.global_lower_bound = 0.0
        self.done = False
        self.node_with_lowest_bound = None
        self.lonely_nodes = None

    def _step(self):
        """One step of the branch-and-bound algorithm.

        Picks node with lowest lower bound, finds a lonely vertex, creates new tree nodes.
        """

        self.all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        self.node_with_lowest_bound = self.all_nodes.pop()

        self.lonely_nodes = self.node_with_lowest_bound.find_lonely_vertices()

        if len(self.lonely_nodes) == 0:
            self.done = True
            return self.node_with_lowest_bound
        else:
            lonely_vertex_chosen = self._choose_lonely_node_highest_degree()

            # choose the right set of possible terminals for this node
            self.node_with_lowest_bound\
                .construct_children_nodes(lonely_vertex_chosen,
                                          self.terminals_by_vertex[lonely_vertex_chosen])

            # note: we do not need to worry about duplicate nodes
            # the nodes are constructed by forcing an assignment of vertices to terminals
            # thus, the resulting partitions can never be identical
            self.all_nodes += self.node_with_lowest_bound.children

            assert (self.node_with_lowest_bound.lower_bound
                    >= self.global_lower_bound), 'lower bound issue'

            self.global_lower_bound = self.node_with_lowest_bound.lower_bound

            return None

    def _choose_lonely_node_random(self):
        lonely_node_list = list(self.lonely_nodes)
        index = np.random.randint(len(lonely_node_list))
        return lonely_node_list[index]

    def _choose_lonely_node_farthest(self):
        used_nodes = set(self.node_with_lowest_bound.graph) - self.lonely_nodes
        shortest_distances = {node: len(self.node_with_lowest_bound.graph)
                              for node in self.node_with_lowest_bound.graph}
        for used_node in used_nodes:
            these_shortest_distances = nx.shortest_path_length(self.node_with_lowest_bound.graph,
                                                               target=used_node)
            for node in self.node_with_lowest_bound.graph:
                shortest_distances[node] = min(shortest_distances[node],
                                               these_shortest_distances[node])
        return max(shortest_distances, key=shortest_distances.get)

    def _choose_lonely_node_highest_degree(self):
        degrees = dict(nx.degree(self.node_with_lowest_bound.graph, weight='capacity'))
        degrees_restricted = {node: node_degree
                              for node, node_degree in degrees.items()
                              if node in self.lonely_nodes}
        return max(degrees_restricted, key=degrees_restricted.get)

    def solve(self, output_flag=False):
        """Solves the multi-terminal cut using the branch-and-bound algorithm.

        Args:
            output_flag: toggles printing of the output

        Returns:
            source_sets: the nodes that remain connected to each terminal
            cut_value: the cost of the multi-terminal cut
        """
        final_node = None
        i = 1
        while not self.done:
            final_node = self._step()
            if output_flag:
                print("Expanding Node Step", i)
                print("Objective Lower Bound", self.global_lower_bound)
                #print("Source Sets Expanded", self.node_with_lowest_bound.source_sets)
            i += 1

        final_node_source_sets = {}
        for terminal in self.terminals:
            if 'combined' in final_node.graph.node[terminal]:
                final_node_source_sets[terminal] = final_node.graph.node[terminal]['combined'] | {terminal}
            else:
                final_node_source_sets[terminal] = {terminal}

        return final_node_source_sets, round(final_node.lower_bound, 8)
