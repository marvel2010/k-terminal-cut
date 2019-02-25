"""Calculates the Minimum Isolating Cut."""

import networkx as nx

from networkx.algorithms.flow import preflow_push


def minimum_isolating_cut(graph, source_vertices, sink_vertices):
    """Compute a minimum isolating cut in G.

    The minimum isolating cut is a cut which separates all the source_nodes from all the sink_nodes.

    Params:
        graph: the graph G in which to compute the minimum isolating cut
        source_vertices: vertices required to fall in the source set
        sink_vertices: vertices required to fall in the sink set

    Returns:
        cut_source: the source set of the isolating cut
        cut_weight: the weight of the isolating cut
    """

    # construct auxiliary graph with super-source and super-sink nodes
    graph.add_nodes_from(["s_node", "t_node"])
    graph.add_edges_from(
        [("s_node", source_adj_node) for source_adj_node in source_vertices]
    )
    graph.add_edges_from([(sink_adj_node, "t_node") for sink_adj_node in sink_vertices])

    # find the residual graph after running a maximum flow algorithm
    residual = preflow_push(graph, "s_node", "t_node")

    # remove the edges which are saturated in the residual graph
    cutset = [
        (u, v, d) for u, v, d in residual.edges(data=True) if d["flow"] >= d["capacity"]
    ]
    residual.remove_edges_from(cutset)

    # the sink set is all nodes which are reachable from the super-sink
    #   after the saturated arcs have been removed
    cut_sink = set(nx.shortest_path_length(residual, target="t_node"))
    # the source set is all the nodes which are not in the sink set
    cut_source = set(graph) - cut_sink

    if cutset is not None:
        residual.add_edges_from(cutset)

    # determine the weight of the resulting minimum cut
    cut_weight = residual.graph["flow_value"]

    assert "s_node" in cut_source, " source node not included in source set "
    assert "t_node" in cut_sink, " sink node not included in sink set "

    cut_source -= {"s_node"}
    cut_sink -= {"t_node"}

    graph.remove_nodes_from(["s_node", "t_node"])

    return cut_source, cut_weight
