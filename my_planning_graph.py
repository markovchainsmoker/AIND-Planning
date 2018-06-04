from aimacode.planning import Action
from aimacode.search import Problem
from aimacode.utils import expr,Expr
from lp_utils import decode_state


class PgNode():
    def __init__(self):
        self.parents = set()
        self.children = set()
        self.mutex = set()

    def is_mutex(self, other) -> bool:
        
        if other in self.mutex:
            return True
        return False

    def show(self):
      
        print("{} parents".format(len(self.parents)))
        print("{} children".format(len(self.children)))
        print("{} mutex".format(len(self.mutex)))


class PgNode_s(PgNode):

    def __init__(self, symbol: Expr, is_pos: bool):

        PgNode.__init__(self)
        self.symbol = symbol
        self.is_pos = is_pos
        self.__hash = None

    def show(self):
        if self.is_pos:
            print("\n*** {}".format(self.symbol))
        else:
            print("\n*** ~{}".format(self.symbol))
        PgNode.show(self)

    def __eq__(self, other):

        return (isinstance(other, self.__class__) and self.is_pos == other.is_pos and self.symbol == other.symbol)

    def __not_eq__(self, other):
        '''inequality test for nodes - compares only the literal for equality

        :param other: PgNode_s
        :return: bool
        '''
        if isinstance(other, self.__class__):
            return (self.symbol == other.symbol) \
                   and (self.is_pos != other.is_pos)

    def __hash__(self):
        self.__hash = self.__hash or hash(self.symbol) ^ hash(self.is_pos)
        return self.__hash


class PgNode_a(PgNode):

    def __init__(self, action: Action):

        PgNode.__init__(self)
        self.action = action
        self.prenodes = self.precond_s_nodes()
        self.effnodes = self.effect_s_nodes()
        self.is_persistent = self.prenodes == self.effnodes
        self.__hash = None

    def show(self):

        print("\n*** {!s}".format(self.action))
        PgNode.show(self)

    def precond_s_nodes(self):

        nodes = set()
        for p in self.action.precond_pos:
            nodes.add(PgNode_s(p, True))
        for p in self.action.precond_neg:
            nodes.add(PgNode_s(p, False))
        return nodes

    def effect_s_nodes(self):

        nodes = set()
        for e in self.action.effect_add:
            nodes.add(PgNode_s(e, True))
        for e in self.action.effect_rem:
            nodes.add(PgNode_s(e, False))
        return nodes

    def __eq__(self, other):

        return (isinstance(other,self.__class__) and
                self.is_persistent == other.is_persistent and
                self.action.name == other.action.name) and (self.action.args == other.action.args)

    def __hash__(self):
        self.__hash = self.__hash or hash(self.action.name) ^ hash(self.action.args)
        return self.__hash
   



def mutexify(node1: PgNode, node2: PgNode):

    if type(node1) != type(node2):
        raise TypeError('Attempted to mutex two nodes of different types')
    node1.mutex.add(node2)
    node2.mutex.add(node1)

def is_effect_mutex(eff1, eff2):
    return True if [e1 for e1 in eff1 if e1 in eff2] else False

class PlanningGraph():
  

    def __init__(self, problem: Problem, state: str, serial_planning=True):
        
        self.problem = problem
        self.fs = decode_state(state, problem.state_map)
        self.serial = serial_planning
        self.all_actions = self.problem.actions_list + self.noop_actions(self.problem.state_map)
        self.s_levels = []
        self.a_levels = []
        self.create_graph()

    def noop_actions(self, literal_list):

        action_list = []
        for fluent in literal_list:
            act1 = Action(expr("Noop_pos({})".format(fluent)), ([fluent], []), ([fluent], []))
            action_list.append(act1)
            act2 = Action(expr("Noop_neg({})".format(fluent)), ([], [fluent]), ([], [fluent]))
            action_list.append(act2)
        return action_list

    def create_graph(self):

        if (len(self.s_levels) != 0) or (len(self.a_levels) != 0):
            raise Exception(
                'Planning Graph already created; construct a new planning graph for each new state in the planning sequence')

        leveled = False
        level = 0
        self.s_levels.append(set())  # S0 set of s_nodes - empty to start
        # for each fluent in the initial state, add the correct literal PgNode_s
        for literal in self.fs.pos:
            self.s_levels[level].add(PgNode_s(literal, True))
        for literal in self.fs.neg:
            self.s_levels[level].add(PgNode_s(literal, False))
        # no mutexes at the first level

        # continue to build the graph alternating A, S levels until last two S levels contain the same literals,
        # i.e. until it is "leveled" 
        while not leveled:
            self.add_action_level(level)
            self.update_a_mutex(self.a_levels[level])

            level += 1
            self.add_literal_level(level)
            self.update_s_mutex(self.s_levels[level])

            if self.s_levels[level] == self.s_levels[level - 1]:
                leveled = True

    def add_action_level(self, level):

        self.a_levels.append(set())
        current_s_nodes = self.s_levels[level]
        count_a_levels_before = len(self.a_levels[level])
        count_subsets = 0; count_total = 0
        for a in self.all_actions:
            a_node = PgNode_a(a)
            if a_node.prenodes.issubset(current_s_nodes):
                for s_node in current_s_nodes:
                    if s_node in a_node.prenodes:
                        s_node.children.add(a_node)
                        a_node.parents.add(s_node)
                self.a_levels[level].add(a_node)
                count_subsets += 1
            count_total += 1
        count_a_levels_after = len(self.a_levels[level])

    def add_literal_level(self, level):
 
        self.s_levels.append(set())
        parent_a_nodes = self.a_levels[level-1]
        count_s_levels_before = len(self.s_levels[level])
        count_unique = 0; count_total = 0
        for parent_a_node in parent_a_nodes:
            effnodes = parent_a_node.effnodes
            for effnode in effnodes:
                is_unique_node = True
                for existing_s_node in self.s_levels[level]:
                    if effnode == existing_s_node:
                        parent_a_node.children.add(existing_s_node)
                        existing_s_node.parents.add(parent_a_node)
                        is_unique_node = False
                if is_unique_node:
                    parent_a_node.children.add(effnode)
                    effnode.parents.add(parent_a_node)
                    self.s_levels[level].add(effnode)
                    count_unique += 1
                count_total += 1
        count_s_levels_after = len(self.s_levels[level])

    def update_a_mutex(self, nodeset):
  
        nodelist = list(nodeset)
        for i, n1 in enumerate(nodelist[:-1]):
            for n2 in nodelist[i + 1:]:
                if (self.serialize_actions(n1, n2) or
                        self.inconsistent_effects_mutex(n1, n2) or
                        self.interference_mutex(n1, n2) or
                        self.competing_needs_mutex(n1, n2)):
                    mutexify(n1, n2)

    def serialize_actions(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
    
        if not self.serial:
            return False
        if node_a1.is_persistent or node_a2.is_persistent:
            return False
        return True

    def inconsistent_effects_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:

        return is_effect_mutex(node_a1.action.effect_add, node_a2.action.effect_rem) or \
               is_effect_mutex(node_a1.action.effect_rem, node_a2.action.effect_add)

    def interference_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:

        return is_effect_mutex(node_a1.action.effect_add, node_a2.action.precond_neg) or \
               is_effect_mutex(node_a1.action.effect_rem, node_a2.action.precond_pos) or \
               is_effect_mutex(node_a2.action.effect_add, node_a1.action.precond_neg) or \
               is_effect_mutex(node_a2.action.effect_rem, node_a1.action.precond_pos)

    def competing_needs_mutex(self, node_a1: PgNode_a, node_a2: PgNode_a) -> bool:
 
        actions_s1 = node_a1.parents
        actions_s2 = node_a2.parents
        return True if [(a1, a2)
                         for a1 in actions_s1
                         for a2 in actions_s2
                         if a1.is_mutex(a2)] \
                    else False

    def update_s_mutex(self, nodeset: set):
        
        nodelist = list(nodeset)
        for i, n1 in enumerate(nodelist[:-1]):
            for n2 in nodelist[i + 1:]:
                if self.negation_mutex(n1, n2) or self.inconsistent_support_mutex(n1, n2):
                    mutexify(n1, n2)

    def negation_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s) -> bool:

        return node_s1.__not_eq__(node_s2)

    def inconsistent_support_mutex(self, node_s1: PgNode_s, node_s2: PgNode_s):
 
        actions_s1 = node_s1.parents
        actions_s2 = node_s2.parents


        return False if [(a1, a2)
                         for a1 in actions_s1
                         for a2 in actions_s2
                         if not a1.is_mutex(a2)] \
                     else True

    def h_levelsum(self) -> int:
 
        level_sum = 0
        for goal in self.problem.goal:
            is_goal = False
            for (level, states) in enumerate(self.s_levels):
                if is_goal:
                    break
                else:
                    for s in states:
 
                        if goal == s.symbol and s.is_pos:
                            level_sum += level

                            is_goal = True
                            break
            if not is_goal:
                return float('Inf')
        return level_sum
