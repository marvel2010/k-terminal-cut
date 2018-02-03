import networkx as nx


def main():
    graph = read_graph('data/email.graph')
    print(len(graph.nodes), len(graph.edges))


def read_graph(filename):
    """Read a graph from a file in the format specified by David Johnson
    for the DIMACS clique challenge.
    Instances are available at
    ftp://dimacs.rutgers.edu/pub/challenge/graph/benchmarks/clique
    """
    graph = nx.Graph()
    f = open(filename)
    count = 0
    for line in f:
        if count:
            for neighbor in line.split():
                graph.add_edge(count, int(neighbor))
        else:
            node_count, edge_count, _ = line.split()
            graph.add_nodes_from(range(1, int(node_count) + 1))
        count += 1
    return graph


if __name__ == '__main__':
    main()