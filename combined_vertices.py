"""Utilities for combining vertices."""


def combined_vertices_several(graph, u, v_set):
    """Combines several vertices"""
    assert u not in v_set, 'cannot combine a node to itself'
    # copy graph
    H = graph.copy()
    # decide if nodes are single or duplicate
    for v in v_set:
        for _, w, d in graph.edges(v, data=True):
            if w == u or w in v_set:
                continue
            elif (u, w) in H.edges(u):
                H[u][w]['capacity'] += d['capacity']
            else:
                H.add_edge(u, w, capacity=d['capacity'])
        H.remove_node(v)
        # keep a record of all contracted nodes
        if 'combined' in H.node[u]:
            H.node[u]['combined'].add(v)
        else:
            H.node[u]['combined'] = {v}
    return H


def combined_vertices(graph, u, v):
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
    # copy graph
    H = graph.copy()
    # decide if nodes are single or duplicate
    for x, w, d in graph.edges(v, data=True):
        if u == w:
            continue
        if (u, w) in H.edges(u):
            H[u][w]['capacity'] += d['capacity']
        else:
            H.add_edge(u, w, capacity=d['capacity'])
    H.remove_node(v)
    # keep a record of all contracted nodes
    if 'combined' in H.node[u]:
        H.node[u]['combined'].add(v)
    else:
        H.node[u]['combined'] = {v}
    return H