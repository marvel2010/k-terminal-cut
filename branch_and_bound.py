import numpy as np
import networkx as nx
from tree_node import TreeNode


def branch_and_bound_algorithm(G, terminals):

    root = TreeNode(None, None, None, is_root=1, in_graph=G, in_terminals=terminals)

    #print("Root Node")
    #print('children ', root.children)
    #print('contained sets ', root.contained_sets)
    #print('iso weights ', root.iso_cut_weights)
    #print('lonely nodes ', root.find_lonely_nodes())

    branch_and_bound_tree = BranchAndBoundTree(root)
    return branch_and_bound_tree.all_steps()


class BranchAndBoundTree:

    def __init__(self, root_node):

        #self.root_node = root_node
        self.all_nodes = [root_node]
        self.global_lower_bound = 0.0
        self.done = 0
        self.node_with_lowest_bound = None
        self.lonely_nodes = None

    def step(self):

        self.all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        self.node_with_lowest_bound = self.all_nodes.pop()

        #print("All Nodes Length", len(self.all_nodes))
        #print("All Nodes", [node.lower_bound for node in self.all_nodes])

        self.lonely_nodes = self.node_with_lowest_bound.find_lonely_nodes()

        if len(self.lonely_nodes) == 0:
            self.done = 1
            return self.node_with_lowest_bound
        else:
            #lonely_node_chosen = self._choose_lonely_node_random()
            #lonely_node_chosen = self._choose_lonely_node_farthest()
            lonely_node_chosen = self._choose_lonely_node_highest_degree()
            self.node_with_lowest_bound.construct_children_nodes(lonely_node_chosen)
            self.all_nodes += self.node_with_lowest_bound.children
            assert self.node_with_lowest_bound.lower_bound >= self.global_lower_bound, 'lower bound issue: lowest so far %s now %s' % (self.global_lower_bound, node_with_lowest_bound.lower_bound)
            self.global_lower_bound = self.node_with_lowest_bound.lower_bound
            # print status
            print("Lonely Node Chosen", lonely_node_chosen)
            print("Lower Bound", self.node_with_lowest_bound.lower_bound)
            print("Contained Sets", self.node_with_lowest_bound.contained_sets)
            print("Lonely Node Count", len(self.lonely_nodes))
            return None

    def _choose_lonely_node_random(self):
        return np.random.choice(list(self.lonely_nodes))

    def _choose_lonely_node_farthest(self):
        used_nodes = set(self.node_with_lowest_bound.graph) - self.lonely_nodes
        shortest_distances = {node: len(self.node_with_lowest_bound.graph) for node in self.node_with_lowest_bound.graph}
        for used_node in used_nodes:
            these_shortest_distances = nx.shortest_path_length(self.node_with_lowest_bound.graph, target=used_node)
            for node in self.node_with_lowest_bound.graph:
                shortest_distances[node] = min(shortest_distances[node], these_shortest_distances[node])
        #print('Shortest Distances', shortest_distances)
        return max(shortest_distances, key=shortest_distances.get)

    def _choose_lonely_node_highest_degree(self):
        degrees = nx.degree(self.node_with_lowest_bound.graph, weight='capacity')
        degrees_restricted = {node: node_degree for node, node_degree in degrees.items() if node in self.lonely_nodes}
        print('Degrees Restricted', degrees_restricted)
        return max(degrees_restricted, key=degrees_restricted.get)

    def all_steps(self):

        final_node = None
        i = 1
        while not self.done:
            print("Expanding Node Step", i)
            final_node = self.step()
            i += 1
            print()
        return final_node
