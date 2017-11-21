"""Solves the LP and IP Formulations of the Multiterminal Cut Problem using Gurobi."""

from gurobipy import Model
from gurobipy import GRB
from gurobipy import quicksum


def ip_algorithm(graph,
                 terminals,
                 relaxation=False,
                 dual=False,
                 persistence_sets=False,
                 print_solution=False):
    """Solves the IP formulation of the Multiterminal Cut Problem using Gurobi.

    Vertex Variables: x_i^k for each vertex i for each set k
    Edge Variables: z_ij^k for each edge (i, j) for each set k

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

    mdl = Model("MultiTerminalCuts")

    # VARIABLES
    x_variables = {}
    z_variables = {}

    # VARIABLE X: node i, set k
    for i in graph.nodes():
        x_variables[i] = {}
        for k in terminals:
            if relaxation:
                x_variables[i][k] = mdl.addVar(vtype=GRB.CONTINUOUS,
                                               lb=0.0,
                                               ub=1.0,
                                               name="Node %s, Terminal %s" % (i, k))
            else:
                x_variables[i][k] = mdl.addVar(vtype=GRB.BINARY,
                                               name="Node %s, Terminal %s" % (i, k))

    # VARIABLE Z: node i, node j, set k
    for i in graph.nodes():
        z_variables[i] = {}
        for j in graph[i]:
            z_variables[i][j] = {}
            for k in terminals:
                if relaxation:
                    z_variables[i][j][k] = mdl.addVar(vtype=GRB.CONTINUOUS,
                                                      lb=0.0,
                                                      ub=1.0,
                                                      obj=0.5*graph[i][j]['capacity'],
                                                      name="Node %s, Node %s, Terminal %s" % (i, j, k))
                else:
                    z_variables[i][j][k] = mdl.addVar(vtype=GRB.BINARY,
                                                      obj=0.5*graph[i][j]['capacity'],
                                                      name="Node %s, Node %s, Terminal %s" % (i, j, k))

    mdl.modelSense = GRB.MINIMIZE
    mdl.update()

    # CONSTRAINTS
    c_nodes = {}
    c_edges = {}
    c_terminals = {}

    # CONSTRAINT: one terminal per node
    for i in graph.nodes():
        c_nodes[i] = mdl.addConstr(quicksum(x_variables[i][k] for k in terminals) == 1.0,
                                   "CtrNode %s" % str(i))

    # CONSTRAINT: price for cut
    for (i, j) in graph.edges():
        c_edges[(i, j)] = {}
        c_edges[(j, i)] = {}
        for k in terminals:
            c_edges[(i, j)][k] = (
                mdl.addConstr(z_variables[i][j][k] >= x_variables[i][k] - x_variables[j][k],
                              name="flow %s %s %s" % (i, j, k))
            )
            c_edges[(j, i)][k] = (
                mdl.addConstr(z_variables[i][j][k] >= x_variables[j][k] - x_variables[i][k],
                              name="flow %s %s %s" % (j, i, k))
            )

    # CONSTRAINT: initialize
    for k in terminals:
        c_terminals[k] = mdl.addConstr(x_variables[k][k] == 1.0, name="Init %s" % k)

    # solve
    mdl.Params.LogToConsole = 0
    mdl.optimize()

    # primal variables
    if print_solution:
        for variable in mdl.getVars():
            if variable.getAttr("x") != 0.0:
                print("value of variable %s, is %s" % (variable.varName,
                                                       variable.getAttr("x")))

    # dual variables
    if dual:
        assert relaxation, 'only get dual of LP relaxation'
        for constraint in mdl.getConstrs():
            if constraint.getAttr("Pi") != 0.0:
                print('value of constraint %s, is %s' % (constraint.constrName,
                                                         constraint.getAttr("Pi")))

    # record solution
    source_sets = {terminal: set() for terminal in terminals}
    possible_terminals_by_node = {node: set() for node in graph.nodes()}
    for i in graph.nodes():
        for k in terminals:
            if x_variables[i][k].x == 1.0:
                source_sets[k].add(i)
            if x_variables[i][k].x > 0.0:
                possible_terminals_by_node[i].add(k)
    cut_value = round(mdl.ObjVal, 8)

    if persistence_sets:
        assert relaxation, 'only get persistence from LP relaxation'
        return possible_terminals_by_node, cut_value
    else:
        return source_sets, cut_value
