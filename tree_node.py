import networkx as nx
from itertools import chain
from copy import deepcopy
import random


def minimum_isolating_cut(G, source_nodes, sink_nodes):

    # construct aux graph
    G_prime = G.copy()
    G_prime.add_nodes_from(['s', 't'])
    # no 'capacity' attribute implies infinite capacity
    G_prime.add_edges_from([('s', source_adj_node) for source_adj_node in source_nodes], capacity=100)
    G_prime.add_edges_from([(sink_adj_node, 't') for sink_adj_node in sink_nodes], capacity=100)
    # run minimum cut
    cut_weight, (cut_source, cut_sink) = nx.minimum_cut(G_prime, 's', 't')

    #print(G_prime)
    #print('some cut source ', source_nodes)
    #print('some cut sink ', sink_nodes)
    #print('some cut weight ', cut_weight)

    cut_source -= {'s'}
    cut_sink -= {'t'}

    return cut_source, cut_weight


class TreeNode:

    def __init__(self, parent_node=None, new_node=None, new_source_set=None,
                 is_root=0, in_graph=None, in_terminals=None):

        if is_root:
            assert parent_node is None and new_node is None and new_source_set is None

            # handle root node
            self.parent_node = None
            self.children = []
            self.graph = in_graph

            self.contained_sets = {}
            self.iso_cut_weights = {}

            # todo : equality
            for i in range(len(in_terminals)):
                cut_source, cut_weight = minimum_isolating_cut(self.graph,
                                                               {in_terminals[i]},
                                                               set(in_terminals)-{in_terminals[i]})
                self.contained_sets[i] = cut_source - {'s'}
                self.iso_cut_weights[i] = cut_weight

            self.lower_bound = 0

        else:
            assert in_graph is None and in_terminals is None

            # define variables
            self.parent_node = parent_node
            self.children = []
            self.graph = parent_node.graph

            self.contained_sets = deepcopy(parent_node.contained_sets)
            self.iso_cut_weights = deepcopy(parent_node.iso_cut_weights)

            self.new_node = new_node
            self.new_source_set = new_source_set
            self.contained_sets[self.new_source_set].add(self.new_node)

            #print("\n New Node")
            #print("Parent Node Source Sets: ", self.parent_node.contained_sets)
            #print("Parent Node Cut Values: ", self.parent_node.iso_cut_weights)
            #print("New Node Added from Parent: ", self.new_node)
            #print("New Source Set Added from Parent: ", self.new_source_set)

            # perform actions
            self.expand_source_set()
            self.lower_bound = self._calculate_lower_bound()
            self.upper_bound = self._calculate_upper_bound()

            #print("Expanded Source Sets: ", self.contained_sets)
            #print("New Cut Values: ", self.iso_cut_weights)

    def _add_child(self, new_node, new_source_set):
        child = TreeNode(self, new_node, new_source_set)
        self.children.append(child)

    def construct_children_nodes(self, lonely_node):
        assert len(self.children) == 0, 'children already created'
        for i in range(len(self.contained_sets)):
            self._add_child(new_node=lonely_node, new_source_set=i)

    def find_lonely_nodes(self):
        lonely_nodes = set(self.graph.nodes()) - set(chain.from_iterable(self.contained_sets.values()))
        return lonely_nodes

    def expand_source_set(self):

        self.contained_sets[self.new_source_set], self.iso_cut_weights[self.new_source_set] = \
            minimum_isolating_cut(self.graph,
                                  source_nodes=self.contained_sets[self.new_source_set],
                                  sink_nodes=set(chain.from_iterable([self.contained_sets[index]
                                              for index in range(len(self.contained_sets))
                                              if index != self.new_source_set]))
                                  )

    def _calculate_lower_bound(self):

        #print("Iso Cut Weights ", self.iso_cut_weights.values())
        return sum(list(self.iso_cut_weights.values())) / 2

    def _calculate_upper_bound(self):

        # todo

        return sum(list(self.iso_cut_weights.values()))
