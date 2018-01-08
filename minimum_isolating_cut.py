"""Calculates the Minimum Isolating Cut."""

import networkx as nx
# from networkx.algorithms.flow import edmonds_karp
from networkx.algorithms.flow import preflow_push
# from networkx.algorithms.flow import shortest_augmenting_path


def minimum_isolating_cut(graph, source_nodes, sink_nodes):
    """Compute a minimum isolating cut in G.

    The minimum isolating cut is a cut which separates all the source_nodes from all the sink_nodes.

    Params:
        graph: the graph G in which to compute the minimum isolating cut
        source_nodes: the nodes which are required to fall in the source set
        sink_nodes: the nodes which are required to fall in the sink set

    Returns:
        cut_source: the source set of the isolating cut
        cut_weight: the weight of the isolating cut
    """

    # construct aux graph
    graph.add_nodes_from(['s_node', 't_node'])
    graph.add_edges_from([('s_node', source_adj_node) for source_adj_node in source_nodes])
    graph.add_edges_from([(sink_adj_node, 't_node') for sink_adj_node in sink_nodes])

    # find minimum cut with maximal source set
    residual = preflow_push(graph, 's_node', 't_node')  # residual graph

    # use >= to deal with float issue
    cutset = [(u, v, d) for u, v, d in residual.edges(data=True) if d['flow'] >= d['capacity']]
    residual.remove_edges_from(cutset)
    cut_sink = set(nx.shortest_path_length(residual, target='t_node'))
    cut_source = set(graph) - cut_sink
    if cutset is not None:
        residual.add_edges_from(cutset)
    cut_weight = residual.graph['flow_value']

    assert 's_node' in cut_source, ' source node not included in source set '
    assert 't_node' in cut_sink, ' sink node not included in sink set '

    cut_source -= {'s_node'}
    cut_sink -= {'t_node'}

    graph.remove_nodes_from(['s_node', 't_node'])

    return cut_source, cut_weight

