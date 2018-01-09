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
        self._terminals = root_node.get_terminals()

        self._terminals_by_vertex = terminals_by_vertex
        self._all_nodes = [BranchAndBoundTreeNode(graph, terminals, None, None)]
        self._global_lower_bound = 0.0
        self._done = False
        self._node_with_lowest_bound = None
        self._lonely_vertices = None

    def _step(self):
        """One step of the branch-and-bound algorithm.

        Picks node with lowest lower bound, finds a lonely vertex, creates new tree nodes.
        """

        self._all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        self._node_with_lowest_bound = self._all_nodes.pop()

        self._lonely_vertices = self._node_with_lowest_bound.find_lonely_vertices()

        if not self._lonely_vertices:
            self._done = True
            return self._node_with_lowest_bound

        else:
            # if there are still lonely vertices
            lonely_vertex_chosen = self._choose_lonely_node_highest_degree()
            # self.print_source_sets()
            # print("Lonely Vertex Chosen %s " % lonely_vertex_chosen)

            # choose the right set of possible terminals for this node
            self._node_with_lowest_bound\
                .construct_children_nodes(lonely_vertex_chosen,
                                          self._terminals_by_vertex[lonely_vertex_chosen])

            # note: we do not need to worry about duplicate nodes
            # the nodes are constructed by forcing an assignment of vertices to terminals
            # thus, the resulting partitions can never be identical
            self._all_nodes += self._node_with_lowest_bound.children

            assert (self._node_with_lowest_bound.lower_bound
                    >= self._global_lower_bound), 'lower bound issue'

            self._global_lower_bound = self._node_with_lowest_bound.lower_bound

            return None

    # def _choose_lonely_node_random(self):
    #     lonely_node_list = list(self._lonely_vertices)
    #     index = np.random.randint(len(lonely_node_list))
    #     return lonely_node_list[index]
    #
    # def _choose_lonely_node_farthest(self):
    #     used_nodes = set(self._node_with_lowest_bound.graph) - self._lonely_vertices
    #     shortest_distances = {node: len(self._node_with_lowest_bound.graph)
    #                           for node in self._node_with_lowest_bound.graph}
    #     for used_node in used_nodes:
    #         these_shortest_distances = nx.shortest_path_length(self._node_with_lowest_bound.graph,
    #                                                            target=used_node)
    #         for node in self._node_with_lowest_bound.graph:
    #             shortest_distances[node] = min(shortest_distances[node],
    #                                            these_shortest_distances[node])
    #     return max(shortest_distances, key=shortest_distances.get)

    def _choose_lonely_node_highest_degree(self):
        degrees = dict(nx.degree(self._node_with_lowest_bound.graph, weight='capacity'))
        degrees_restricted = {node: node_degree
                              for node, node_degree in degrees.items()
                              if node in self._lonely_vertices}
        return max(degrees_restricted, key=degrees_restricted.get)

    def print_source_sets(self):
        for terminal in self._terminals:
            print("Source Sets for Terminal %s" % terminal,
                  self._node_with_lowest_bound.graph.nodes[terminal])

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
        while not self._done:
            final_node = self._step()
            if output_flag:
                print("Expanding Node Step", i)
                print("Objective Lower Bound", self._global_lower_bound)
                self.print_source_sets()
                print()
            i += 1

        final_node_source_sets = {}
        for terminal in self._terminals:
            if 'combined' in final_node.graph.node[terminal]:
                final_node_source_sets[terminal] = (final_node.graph.node[terminal]['combined']
                                                    | {terminal})
            else:
                final_node_source_sets[terminal] = {terminal}

        return final_node_source_sets, round(final_node.lower_bound, 8)
