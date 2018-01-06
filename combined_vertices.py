"""Utilities for combining vertices."""


def combined_vertices_several(graph, u, v_set):
    """Combines several vertices"""
    H = graph.copy()
    for v in v_set:
        H = combined_vertices(H, u, v)
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
    if 'contraction' in H.node[u]:
        H.node[u]['contraction'].add(v)
    else:
        H.node[u]['contraction'] = {v}
    return H