"""Utilities for combining vertices."""


def contract_vertices_several(graph, u, v_set):
    """Combines several vertices"""
    assert u not in v_set, 'cannot combine a node to itself'
    # decide if nodes are single or duplicate
    for v in v_set:
        for _, w, d in graph.edges(v, data=True):
            if w == u or w in v_set:
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


def contract_vertex_and_copy(graph, u, v):
    """
    Combined two nodes in a graph such that their outgoing capacities sum.

    Input:
        graph
        u
        v

    Output:
        new_graph
    """
    assert u != v, 'cannot combine a node to itself'
    # copy
    H = graph.copy()
    # decide if nodes are single or duplicate
    for _, w, d in graph.edges(v, data=True):
        if w == u:
            continue
        elif (u, w) in H.edges(u):
            H[u][w]['capacity'] += d['capacity']
        else:
            H.add_edge(u, w, capacity=d['capacity'])
    # remove node
    H.remove_node(v)
    # keep a record of all contracted nodes
    if 'combined' in H.node[u]:
        H.node[u]['combined'].add(v)
    else:
        H.node[u]['combined'] = {v}
    return H