"""Read data."""


def test_read_dimacs():
    from ktcut.read_data import read_dimacs_graph
    graph = read_dimacs_graph('data/dimacs/jazz.graph')
    assert len(graph.nodes) == 198
    assert len(graph.edges) == 2742


def test_read_konect():
    from ktcut.read_data import read_konect_graph
    graph = read_konect_graph('data/konect/out.arenas-jazz')
    assert len(graph.nodes) == 198
    assert len(graph.edges) == 2742
