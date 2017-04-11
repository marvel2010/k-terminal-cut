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
        self.done = 0

    def step(self):

        self.all_nodes.sort(key=lambda x: x.lower_bound, reverse=True)
        node_with_lowest_bound = self.all_nodes.pop()

        lonely_nodes = node_with_lowest_bound.find_lonely_nodes()

        if len(lonely_nodes) == 0:
            self.done = 1
            #print("Lower Bound", node_with_lowest_bound.lower_bound)
            return node_with_lowest_bound
        else:
            #print("Lonely Nodes ", lonely_nodes)
            node_with_lowest_bound.construct_children_nodes(np.random.choice(list(lonely_nodes)))
            self.all_nodes += node_with_lowest_bound.children
            print("Lower Bound", node_with_lowest_bound.lower_bound)
            return None

    def all_steps(self):

        final_node = None
        i = 1
        while not self.done:
            print("Step", i)
            final_node = self.step()
            i += 1
        return final_node
