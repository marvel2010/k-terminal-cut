"""LP and IP Formulations of the k-Terminal Cut Problem."""

import pulp
from pulp import LpProblem
from pulp import LpMinimize
from pulp import LpVariable
from pulp import LpInteger
from pulp import LpContinuous
from pulp import lpSum
from pulp import value


class IPFormulation:
    """Formulates the k-Terminal Cut Problem as an Integer Program.

    Vertex Variables: x_i^k for each vertex i for each set k
    Edge Variables: z_ij^k for each edge (i, j) for each set k

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k
    """

    def __init__(self, graph, terminals, solver=None):
        self.graph = graph
        self.terminals = terminals
        self.mdl = None
        self.x_variables = {}
        self.z_variables = {}
        self.possible_terminals_by_node_weak = None
        self.possible_terminals_by_node_strong = None
        self.source_sets = None
        self.cut_value = None
        self.solver = solver

    def _initialize_model(self):
        self.mdl = LpProblem("MultiTerminalCuts", LpMinimize)

    def _initialize_node_variables_ip(self):
        """
        Initialize variables x_i^k for IP.
        """
        for i in self.graph.nodes():
            self.x_variables[i] = {}
            for k in self.terminals:
                self.x_variables[i][k] = LpVariable(
                    "n %s, t %s" % (i, k), 0, 1, LpInteger
                )

    def _initialize_node_variables_lp(self):
        """
        Initialize variables x_i^k for LP.
        """
        for i in self.graph.nodes():
            self.x_variables[i] = {}
            for k in self.terminals:
                self.x_variables[i][k] = LpVariable(
                    "n %s, t %s" % (i, k), 0, 1, LpContinuous
                )

    def _initialize_edge_variables_ip(self):
        """
        Initialize variables z_ij^k for IP.
        """
        for i in self.graph.nodes():
            self.z_variables[i] = {}
            for j in self.graph[i]:
                self.z_variables[i][j] = {}
                for k in self.terminals:
                    self.z_variables[i][j][k] = LpVariable(
                        "n %s, n %s, t %s" % (i, j, k), 0, 1, LpInteger
                    )

    def _initialize_edge_variables_lp(self):
        """
        Initialize variables z_ij^k for LP.
        """
        for i in self.graph.nodes():
            self.z_variables[i] = {}
            for j in self.graph[i]:
                self.z_variables[i][j] = {}
                for k in self.terminals:
                    self.z_variables[i][j][k] = LpVariable(
                        "n %s, n %s, t %s" % (i, j, k), 0, 1, LpContinuous
                    )

    def _initialize_objective(self):
        """
        Initialize objective
        """
        self.mdl += lpSum(
            0.5 * self.graph[i][j]["capacity"] * self.z_variables[i][j][k]
            for (i, j) in self.graph.edges
            for k in self.terminals
        )

    def _initialize_contraint_nodes(self):
        """
        Initialize constraint sum_k{x_{i}^k} = 1
        """
        for i in self.graph.nodes():
            self.mdl += (
                (sum(self.x_variables[i][k] for k in self.terminals) == 1.0),
                "sumNode %s" % str(i),
            )

    def _initialize_constraint_edges(self):
        """
        Initialize constrants
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k
        """
        for (i, j) in self.graph.edges():
            for k in self.terminals:
                self.mdl += (
                    (
                        self.z_variables[i][j][k]
                        >= self.x_variables[i][k] - self.x_variables[j][k]
                    ),
                    "flow %s %s %s" % (i, j, k),
                )
                self.mdl += (
                    (
                        self.z_variables[i][j][k]
                        >= self.x_variables[j][k] - self.x_variables[i][k]
                    ),
                    "flow %s %s %s" % (j, i, k),
                )

    def _initialize_constraint_terminals(self):
        """
        Initialize constraint
            x_k^k = 1
        """
        for k in self.terminals:
            self.mdl += (self.x_variables[k][k] == 1.0), "init %s" % k

    def _run_solver(self):
        if self.solver is None:
            self.mdl.solve()
        else:
            self.mdl.solve(self.solver)

    def _calculate_possible_terminals_by_node_weak(self):
        """
        record solution: possible terminals by node assuming *weak* persistence
        """
        self.possible_terminals_by_node_weak = {
            node: set() for node in self.graph.nodes()
        }
        for i in self.graph.nodes():
            flag = True
            for k in self.terminals:
                if round(self.x_variables[i][k].varValue, 5) == 1.0:
                    self.possible_terminals_by_node_weak[i].add(k)
                    flag = False
            if flag:
                self.possible_terminals_by_node_weak[i] = self.terminals

    def _calculate_possible_terminals_by_node_strong(self):
        """
        record solution: possible terminals by node assuming *strong* persistence
        """
        self.possible_terminals_by_node_strong = {
            node: set() for node in self.graph.nodes()
        }
        for i in self.graph.nodes():
            for k in self.terminals:
                if self.x_variables[i][k].varValue > 0.0:
                    self.possible_terminals_by_node_strong[i].add(k)

    def _calculate_source_sets(self):
        """
        record solution: source sets
        """
        self.source_sets = {terminal: set() for terminal in self.terminals}
        for i in self.graph.nodes():
            for k in self.terminals:
                if round(self.x_variables[i][k].varValue, 5) == 1.0:
                    self.source_sets[k].add(i)

    def _calculate_cut_value(self):
        """calculate: self.cut_value"""
        self.cut_value = round(value(self.mdl.objective), 5)

    def get_cut_value(self):
        """get: self.cut_value"""
        return self.cut_value

    def get_possible_terminals_by_node_weak(self):
        """get: self.possible_terminals_by_node_weak"""
        return self.possible_terminals_by_node_weak

    def get_possible_terminals_by_node_strong(self):
        """get: self.possible_terminals_by_node_strong"""
        return self.possible_terminals_by_node_strong

    def get_source_sets(self):
        """get: self.source_sets"""
        return self.source_sets

    def solve_ip(self):
        """Solves the Integer Program."""
        self._initialize_model()
        self._initialize_node_variables_ip()
        self._initialize_edge_variables_ip()
        self._initialize_objective()
        self._initialize_contraint_nodes()
        self._initialize_constraint_edges()
        self._initialize_constraint_terminals()
        self._run_solver()
        self._calculate_cut_value()
        self._calculate_source_sets()

    def solve_lp(self):
        """Solves the Linear Program."""
        self._initialize_model()
        self._initialize_node_variables_lp()
        self._initialize_edge_variables_lp()
        self._initialize_objective()
        self._initialize_contraint_nodes()
        self._initialize_constraint_edges()
        self._initialize_constraint_terminals()
        self._run_solver()
        self._calculate_cut_value()
        self._calculate_source_sets()
        self._calculate_possible_terminals_by_node_weak()
        self._calculate_possible_terminals_by_node_strong()
