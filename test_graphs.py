from branch_and_bound import branch_and_bound_algorithm
import networkx as nx


def main():
    G = nx.Graph()

    G.add_nodes_from([i for i in range(1, 9)])
    G.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)], capacity=2)
    G.add_edges_from([(1, 5), (2, 6), (3, 7), (4, 8)], capacity=3)

    final_node = branch_and_bound_algorithm(G, [1, 2, 3, 4])

    print('Final')
    print('Final Sets ', final_node.contained_sets)
    print('Final Value ', final_node.lower_bound)

if __name__ == '__main__':
    main()
