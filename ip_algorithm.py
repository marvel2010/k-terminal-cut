"""Solves the LP and IP Formulations of the Multiterminal Cut Problem using Gurobi."""

from ip_formulation import IPFormulation


def ip_algorithm(graph,
                 terminals,
                 relaxation=False,
                 persistence_sets=False):
    """Solves the IP formulation of the Multiterminal Cut Problem using Gurobi.

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k

    Args:
        graph: The networkx graph for which the Multiterminal Cut Problem is to be solved.
        terminals: The nodes which are terminals in the Multiterminal Cut Problem.
        relaxation: Solves the LP relaxation instead of the full IP.
        dual: Includes information about the LP dual.
        persistence_sets: Returns the terminals_by_vertex mapping.
        print_solution: Prints solution to output.

    Returns:
        dictionary of terminal to nodes associated with terminal.
        value of the IP or LP cut.
    """

    ip_formulation = IPFormulation(graph, terminals)

    if relaxation:
        ip_formulation.solve_lp()
        if persistence_sets:
            return ip_formulation.get_possible_terminals_by_node(), ip_formulation.get_cut_value()
    else:
        ip_formulation.solve_ip()
    return ip_formulation.get_source_sets(), ip_formulation.get_cut_value()