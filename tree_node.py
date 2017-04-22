import networkx as nx
from itertools import chain
from copy import deepcopy
from networkx.algorithms.flow import shortest_augmenting_path, preflow_push, edmonds_karp


def minimum_isolating_cut(G, source_nodes, sink_nodes):

    # construct aux graph
    G_prime = G.copy()
    G_prime.add_nodes_from(['s_node', 't_node'])

    # no 'capacity' attribute implies infinite capacity
    G_prime.add_edges_from([('s_node', source_adj_node) for source_adj_node in source_nodes])
    G_prime.add_edges_from([(sink_adj_node, 't_node') for sink_adj_node in sink_nodes])

    # find minimum cut with maximal source set
    R = preflow_push(G_prime, 's_node', 't_node')  # residual graph
    # use >= to deal with float issue
    cutset = [(u, v, d) for u, v, d in R.edges(data=True) if d['flow'] >= d['capacity']]
    R.remove_edges_from(cutset)
    cut_sink = set(nx.shortest_path_length(R, target='t_node'))
    cut_source = set(G_prime) - cut_sink
    if cutset is not None:
        R.add_edges_from(cutset)
    cut_weight = R.graph['flow_value']

    #cut_weight, cut_partition = nx.minimum_cut(G_prime, 's_node', 't_node', capacity='capacity', flow_func=shortest_augmenting_path)
    #cut_source, cut_sink = cut_partition

    #print('PreflowPush', nx.minimum_cut(G_prime, 's_node', 't_node', flow_func=preflow_push))
    #print('ShortestAugPath', nx.minimum_cut(G_prime, 's_node', 't_node', flow_func=shortest_augmenting_path))
    #print('EdmondsKarp', nx.minimum_cut(G_prime, 's_node', 't_node', flow_func=edmonds_karp))

    #print('--- requested source nodes', source_nodes)
    #print('--- requested sink nodes', sink_nodes)
    #print('--- returned source', cut_source)
    #print('--- returned sink', cut_sink)
    #print('--- cut weight', cut_weight)

    assert 's_node' in cut_source, ' source node not included in source set '
    assert 't_node' in cut_sink, ' sink node not included in sink set '

    cut_source -= {'s_node'}
    cut_sink -= {'t_node'}

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

            for terminal in in_terminals:

                cut_source, cut_weight = minimum_isolating_cut(self.graph,
                                                               {terminal},
                                                               set(in_terminals)-{terminal})
                self.contained_sets[terminal] = cut_source - {'s'}
                self.iso_cut_weights[terminal] = cut_weight

            self.lower_bound = sum(self.iso_cut_weights.values()) / 2

            for terminal in self.contained_sets:
                # check that every terminal set contains its terminal
                assert terminal in self.contained_sets[terminal], ' init without contained terminals '
                for terminal2 in self.contained_sets:
                    if terminal != terminal2:
                        # check that pairs of terminal sets do not contain overlap
                        assert len(self.contained_sets[terminal] & self.contained_sets[terminal2]) == 0, ' init with overlap '

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

            #print("New Node")
            #print("Parent Source Sets: ", self.parent_node.contained_sets)
            #print("Parent Cut Values: ", self.parent_node.iso_cut_weights)

            # perform actions
            self.expand_source_set()
            self.lower_bound = self._calculate_lower_bound()

            #print("New Source Sets: ", self.contained_sets)
            #print("New Cut Values: ", self.iso_cut_weights)

            assert self.contained_sets[self.new_source_set] > self.parent_node.contained_sets[self.new_source_set], ' subset problem '

    def _add_child(self, new_node, new_source_set):
        child = TreeNode(self, new_node, new_source_set)
        assert child.lower_bound >= self.lower_bound, ' created bad child '
        self.children.append(child)

    def construct_children_nodes(self, lonely_node):
        assert len(self.children) == 0, 'children already created'
        for terminal in self.contained_sets.keys():
            self._add_child(new_node=lonely_node, new_source_set=terminal)

    def find_lonely_nodes(self):
        lonely_nodes = set(self.graph.nodes()) - set(chain.from_iterable(self.contained_sets.values()))
        return lonely_nodes

    def expand_source_set(self):

        self.contained_sets[self.new_source_set], self.iso_cut_weights[self.new_source_set] = \
            minimum_isolating_cut(self.graph,
                                  source_nodes=self.contained_sets[self.new_source_set],
                                  sink_nodes=set(chain.from_iterable([self.contained_sets[index]
                                              for index in self.contained_sets.keys()
                                              if index != self.new_source_set]))
                                  )

    def _calculate_lower_bound(self):

        #print("Iso Cut Weights ", self.iso_cut_weights.values())
        #print("Iso Cut Parents ", self.parent_node.lower_bound)
        return sum(list(self.iso_cut_weights.values())) / 2