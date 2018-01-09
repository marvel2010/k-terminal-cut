"""Utilities for contracting vertices."""


def contract_vertices_several(graph, node_u, v_set):
    """
    Contracts nodes in v_set to u in a graph. The resulting capacity of edges
        from u to w is the sum of the capacities from u and v_set to w. Stores a list
        of contracted nodes at u.

    Args:
        graph: an undirected networkx graph
        u: a node in the graph
        v_set: a set of node in the graph to be contracted into u and removed

    Returns:
        graph: the original graph
    """
    assert node_u not in v_set, 'cannot combine a node to itself'

    for node_v in v_set:
        for _, node_w, data_dict in graph.edges(node_v, data=True):
            if node_w == node_u or node_w in v_set:
                continue
            elif (node_u, node_w) in graph.edges(node_u):
                graph[node_u][node_w]['capacity'] += data_dict['capacity']
            else:
                graph.add_edge(node_u, node_w, capacity=data_dict['capacity'])
        # remove node
        graph.remove_node(node_v)
        # keep a record of all contracted nodes
    if 'combined' in graph.node[node_u]:
        graph.node[node_u]['combined'] |= v_set
    else:
        graph.node[node_u]['combined'] = v_set
    return graph


def contract_vertex(graph, u, v):
    """
    Copies a graph, then contracts nodes v to node u in the copy. The resulting capacity
        of edges from u to w is the sum of the capacities from u and v to w. Stores a list
        of contracted nodes at u.

    Args:
        graph: an undirected networkx graph
        u: a node in the graph
        v: a node in the graph to be contracted into u and removed

    Returns:
        new_graph: a copy of the original graph
    """
    assert u != v, 'cannot combine a node to itself'

    for _, w, d in graph.edges(v, data=True):
        if w == u:
            continue
        elif (u, w) in graph.edges(u):
            graph[u][w]['capacity'] += d['capacity']
        else:
            graph.add_edge(u, w, capacity=d['capacity'])
    # remove node
    graph.remove_node(v)
    # keep a record of all contracted nodes
    if 'combined' in graph.node[u]:
        graph.node[u]['combined'].add(v)
    else:
        graph.node[u]['combined'] = {v}
    return graph
