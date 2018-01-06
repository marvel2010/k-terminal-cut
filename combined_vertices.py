def combined_vertices(G, u, v):
    # copy graph
    H = G.copy()
    # decide if nodes are single or duplicate
    for x, w, d in G.edges(v, data=True):
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