import networkx as nx


def read_dimacs_graph(filename):
    """Read a graph from DIMACS format.

    Row 0: node_count, edge_count, _
    Row 1+: adjacency list

    Args:
        filename: The path of the file to be read.

    Returns:
        graph: The undirected, unweighted graph.
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


def read_konect_graph(filename):
    """Read a graph from KONECT format.

    The KONECT format is as follows:
        % sym unweighted
        node_1 node_2

    Args:
        filename: The path of the file to be read.

    Returns:
        graph: The undirected, unweighted graph.
    """

    # reading phase
    filereader = open(filename)

    # graph properties
    graph_info = filereader.readline().strip("\n").split(" ")
    assert graph_info[0] == "%"
    assert graph_info[1] == "sym"
    assert graph_info[2] == "unweighted"

    graph = nx.Graph()

    for line_edge in filereader:
        line_edge = (
            line_edge.strip("\n")
            .replace("  ", " ")
            .replace("\t", " ")
            .split(" ")
        )
        graph.add_edge(int(line_edge[0]), int(line_edge[1]))

    graph.remove_edges_from(nx.selfloop_edges(graph))

    return graph
