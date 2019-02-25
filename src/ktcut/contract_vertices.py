"""Utilities for contracting vertices in a graph while adding capacities of adjacent edges."""


def contract_vertices(graph, u, v_set):
    """Contracts several vertices.

    Contracts vertices in v_set to u in a graph. The resulting capacity of edges
        from u to w is the sum of the capacities from u and v_set to w. Stores a list
        of contracted vertices at u.

    Args:
        graph: an undirected networkx graph
        u: a vertex in the graph
        v_set: a set of vertices in the graph to be contracted into u and removed

    Returns:
        graph: the original graph after modifications
    """
    assert u not in v_set, "cannot combine a vertex to itself."

    for node_v in v_set:
        for _, node_w, data_dict in graph.edges(node_v, data=True):
            if node_w == u or node_w in v_set:
                continue
            elif (u, node_w) in graph.edges(u):
                graph[u][node_w]["capacity"] += data_dict["capacity"]
            else:
                graph.add_edge(u, node_w, capacity=data_dict["capacity"])
        graph.remove_node(node_v)

    if "combined" in graph.node[u]:
        graph.node[u]["combined"] |= v_set
    else:
        graph.node[u]["combined"] = v_set

    return graph


def contract_vertex(graph, u, v):
    """Contracts a single vertex.

    Contracts vertex v to vertex u in the graph. The resulting capacity of edges from u to w is
        the sum of the capacities from u and v to w. Stores a list of contracted nodes at u.

    Args:
        graph: an undirected networkx graph
        u: a vertex in the graph
        v: a vertex in the graph to be contracted into u and removed

    Returns:
        graph: the original graph after modifications
    """
    assert u != v, "cannot combine a node to itself"

    for _, w, d in graph.edges(v, data=True):
        if w == u:
            continue
        elif (u, w) in graph.edges(u):
            graph[u][w]["capacity"] += d["capacity"]
        else:
            graph.add_edge(u, w, capacity=d["capacity"])

    graph.remove_node(v)

    if "combined" in graph.node[u]:
        graph.node[u]["combined"].add(v)
    else:
        graph.node[u]["combined"] = {v}

    return graph
