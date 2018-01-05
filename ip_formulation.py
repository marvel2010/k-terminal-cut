"""Formulates the LP and IP Formulations of the Multiterminal Cut Problem using Gurobi."""

from gurobipy import Model
from gurobipy import GRB
from gurobipy import quicksum


class IPFormulation():
    """Formulates the Multiterminal Cut Porblem using IP.

    Vertex Variables: x_i^k for each vertex i for each set k
    Edge Variables: z_ij^k for each edge (i, j) for each set k

    minimize (1/2) sum_{i,j,k}{z_{ij}^k}
        such that
            sum_k{x_{i}^k} = 1
            z_{ij}^k >= x_{i}^k-x_{j}^k for all k
            z_{ij}^k >= x_{j}^k-x_{i}^k for all k
    """

    def __init__(self, graph, terminals):
        self.graph = graph
        self.terminals = terminals

    def _initialize_model(self):
        self.mdl = Model("MultiTerminalCuts")

    def _initialize_node_variables_ip(self):
        self.x_variables = {}
        for i in self.graph.nodes():
            self.x_variables[i] = {}
            for k in self.terminals:
                self.x_variables[i][k] = self.mdl.addVar(vtype=GRB.BINARY,
                                                         name="Node %s, Terminal %s" % (i, k))

    def _initialize_node_variables_lp(self):
        self.x_variables = {}
        for i in self.graph.nodes():
            self.x_variables[i] = {}
            for k in self.terminals:
                self.x_variables[i][k] = self.mdl.addVar(vtype=GRB.CONTINUOUS,
                                                         lb=0.0,
                                                         ub=1.0,
                                                         name="Node %s, Terminal %s" % (i, k))

    def _initialize_edge_variables_ip(self):
        self.z_variables = {}
        for i in self.graph.nodes():
            self.z_variables[i] = {}
            for j in self.graph[i]:
                self.z_variables[i][j] = {}
                for k in self.terminals:
                    self.z_variables[i][j][k] = self.mdl.addVar(vtype=GRB.BINARY,
                                                                obj=0.5*self.graph[i][j]['capacity'],
                                                                name="Node %s, Node %s, Terminal %s" % (i, j, k))

    def _initialize_edge_variables_lp(self):
        self.z_variables = {}
        for i in self.graph.nodes():
            self.z_variables[i] = {}
            for j in self.graph[i]:
                self.z_variables[i][j] = {}
                for k in self.terminals:
                    self.z_variables[i][j][k] = self.mdl.addVar(vtype=GRB.CONTINUOUS,
                                                                lb=0.0,
                                                                ub=1.0,
                                                                obj=0.5*self.graph[i][j]['capacity'],
                                                                name="Node %s, Node %s, Terminal %s" % (i, j, k))

    def _initialize_model_sense(self):
        self.mdl.modelSense = GRB.MINIMIZE

    def _initialize_model_update(self):
        self.mdl.update()

    def _initialize_contraint_nodes(self):
        self.c_nodes = {}
        for i in self.graph.nodes():
            self.c_nodes[i] = self.mdl.addConstr(quicksum(self.x_variables[i][k] for k in self.terminals) == 1.0,
                                                 "CtrNode %s" % str(i))

    def _initialize_constraint_edges(self):
        self.c_edges = {}
        for (i, j) in self.graph.edges():
            self.c_edges[(i, j)] = {}
            self.c_edges[(j, i)] = {}
            for k in self.terminals:
                self.c_edges[(i, j)][k] = (
                    self.mdl.addConstr(self.z_variables[i][j][k] >= self.x_variables[i][k] - self.x_variables[j][k],
                                       name="flow %s %s %s" % (i, j, k))
                )
                self.c_edges[(j, i)][k] = (
                    self.mdl.addConstr(self.z_variables[i][j][k] >= self.x_variables[j][k] - self.x_variables[i][k],
                                       name="flow %s %s %s" % (j, i, k))
                )

    # CONSTRAINT: initialize
    def _initialize_constraint_terminals(self):
        self.c_terminals = {}
        for k in self.terminals:
            self.c_terminals[k] = self.mdl.addConstr(self.x_variables[k][k] == 1.0, name="init %s" % k)

    # solve
    def _run_solver(self):
        self.mdl.Params.LogToConsole = 0
        self.mdl.optimize()

    # record solution: source sets
    def _calculate_source_sets(self):
        self.source_sets = {terminal: set() for terminal in self.terminals}
        for i in self.graph.nodes():
            for k in self.terminals:
                if self.x_variables[i][k].x == 1.0:
                    self.source_sets[k].add(i)

    # record solution: possible terminals by node
    def _calculate_possible_terminals_by_node(self):
        self.possible_terminals_by_node = {node: set() for node in self.graph.nodes()}
        for i in self.graph.nodes():
            for k in self.terminals:
                if self.x_variables[i][k].x > 0.0:
                    self.possible_terminals_by_node[i].add(k)

    # record solution: cut value
    def _calculate_cut_value(self):
        self.cut_value = round(self.mdl.ObjVal, 8)

    # primal variables
    def print_primal(self):
        for variable in self.mdl.getVars():
            if variable.getAttr("x") != 0.0:
                print("value of variable %s, is %s" % (variable.varName,
                                                       variable.getAttr("x")))

    # dual variables
    def print_dual(self):
        for constraint in self.mdl.getConstrs():
            if constraint.getAttr("Pi") != 0.0:
                print('value of constraint %s, is %s' % (constraint.constrName,
                                                         constraint.getAttr("Pi")))

    # get cut value
    def get_cut_value(self):
        return self.cut_value

    # get source sets
    def get_source_sets(self):
        return self.source_sets

    # get possible terminals by node
    def get_possible_terminals_by_node(self):
        return self.possible_terminals_by_node

    def solve_ip(self):
        self._initialize_model()
        self._initialize_node_variables_ip()
        self._initialize_edge_variables_ip()
        self._initialize_contraint_nodes()
        self._initialize_constraint_edges()
        self._initialize_constraint_terminals()
        self._initialize_model_sense()
        self._initialize_model_update()
        self._run_solver()
        self._calculate_source_sets()
        self._calculate_possible_terminals_by_node()
        self._calculate_cut_value()

    def solve_lp(self):
        self._initialize_model()
        self._initialize_node_variables_lp()
        self._initialize_edge_variables_lp()
        self._initialize_contraint_nodes()
        self._initialize_constraint_edges()
        self._initialize_constraint_terminals()
        self._initialize_model_sense()
        self._initialize_model_update()
        self._run_solver()
        self._calculate_source_sets()
        self._calculate_possible_terminals_by_node()
        self._calculate_cut_value()