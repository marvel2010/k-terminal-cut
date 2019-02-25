"""Defines a Node in the Branch and Bound Tree for Isolation Branching."""
from copy import deepcopy
from ktcut.contract_vertices import contract_vertex
from ktcut.contract_vertices import contract_vertices
from ktcut.minimum_isolating_cut import minimum_isolating_cut


class IsolationBranchingNode:
    """Node in the isolation branching tree for k-terminal cut.

    Attributes:
        input_graph: a graph in which all previous isolating cuts
            have been merged to terminals
        input_terminals: terminals in the graph
        new_vertex: the lonely vertex to add to a terminal
            from the parent node
        new_vertex_terminal: the terminal to add the lonely vertex
            from the parent node
    """

    def __init__(
        self,
        input_graph,
        input_terminals,
        new_vertex,
        new_vertex_terminal,
        depth=0,
    ):

        # deep copy at this level is important
        self.graph = deepcopy(input_graph)
        self.terminals = input_terminals
        self.new_vertex = new_vertex
        self.new_vertex_terminal = new_vertex_terminal
        self.depth = depth

        self.children = []

        # run expansions
        if self.new_vertex is not None and self.new_vertex_terminal is not None:
            self._source_set_add_vertex()
            self._source_set_isolating_cut()

        terminal_terminal_capacity, terminal_vertex_capacity = self._sum_of_terminal_adjacent_edges()

        self.lower_bound = terminal_terminal_capacity + terminal_vertex_capacity / 2.0
        self.upper_bound = terminal_terminal_capacity + terminal_vertex_capacity

    def _source_set_add_vertex(self):
        # copy required because we try adding the same vertex
        # to several source sets
        self.graph = contract_vertex(
            self.graph, self.new_vertex_terminal, self.new_vertex
        )

    def _source_set_isolating_cut(self):
        source_set, weight = minimum_isolating_cut(
            self.graph,
            source_vertices={self.new_vertex_terminal},
            sink_vertices=set(self.terminals) - {self.new_vertex_terminal},
        )
        self.graph = contract_vertices(
            self.graph,
            self.new_vertex_terminal,
            source_set - {self.new_vertex_terminal},
        )

    def _construct_child_node(self, new_vertex, new_vertex_terminal):
        """Creates a new child of this tree node.

        Creates a new child of this tree node by adding new_node to
            the source set of new_vertex_terminal.

        Params:
            new_node: the node to be added (previously lonely)
            new_source_set: the set this new node will be added to
        """
        child = IsolationBranchingNode(
            self.graph,
            self.terminals,
            new_vertex,
            new_vertex_terminal,
            depth=self.depth + 1,
        )
        assert child.lower_bound >= self.lower_bound, "created bad child."
        self.children.append(child)

    def _sum_of_terminal_adjacent_edges(self):
        """Sum of capacities of edges adjacent to terminals.

        Returns:
            terminal_terminal_capacity_sum: total weight of edges between
                pairs of terminals.
            terminal_vertex_capacity_sum: total weight of edges between a
                terminal and a non-terminal vertex.
        """
        terminal_terminal_capacity_sum = 0.0
        terminal_vertex_capacity_sum = 0.0
        for terminal in self.terminals:
            neighbors = self.graph[terminal]
            for neighbor in neighbors:
                if neighbor in self.terminals:
                    terminal_terminal_capacity_sum += self.graph[terminal][neighbor]["capacity"]
                else:
                    terminal_vertex_capacity_sum += self.graph[terminal][neighbor]["capacity"]
        return terminal_terminal_capacity_sum / 2.0, terminal_vertex_capacity_sum

    def construct_children_nodes(self, unassigned_vertex, allowed_terminals):
        """Runs _add_child for each possible source set."""
        assert not self.children, "children already created"
        for terminal in allowed_terminals:
            self._construct_child_node(new_vertex=unassigned_vertex, new_vertex_terminal=terminal)

    @property
    def unassigned_vertices(self) -> set:
        """Finds the vertices in the graph which are unassigned."""
        unassigned_vertices = set(self.graph.nodes()) - set(self.terminals)
        return unassigned_vertices
