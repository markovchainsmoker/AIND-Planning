from aimacode.logic import PropKB
from aimacode.planning import Action
from aimacode.search import (
    Node, breadth_first_search, astar_search, depth_first_graph_search,
    uniform_cost_search, greedy_best_first_graph_search, Problem,
)
from aimacode.utils import expr
from lp_utils import (
    FluentState, encode_state, decode_state
)
from my_planning_graph import PlanningGraph
from run_search import run_search

from functools import lru_cache


class HaveCakeProblem(Problem):
    def __init__(self, initial: FluentState, goal: list):
        self.state_map = initial.pos + initial.neg
        Problem.__init__(self, encode_state(initial, self.state_map), goal=goal)
        self.actions_list = self.get_actions()

    def get_actions(self):
        precond_pos = [expr("Have(Cake)")]
        precond_neg = []
        effect_add = [expr("Eaten(Cake)")]
        effect_rem = [expr("Have(Cake)")]
        eat_action = Action(expr("Eat(Cake)"),
                            [precond_pos, precond_neg],
                            [effect_add, effect_rem])
        precond_pos = []
        precond_neg = [expr("Have(Cake)")]
        effect_add = [expr("Have(Cake)")]
        effect_rem = []
        bake_action = Action(expr("Bake(Cake)"),
                             [precond_pos, precond_neg],
                             [effect_add, effect_rem])
        return [eat_action, bake_action]

    def actions(self, state: str) -> list:  # of Action
        possible_actions = []
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for action in self.actions_list:
            is_possible = True
            for clause in action.precond_pos:
                if clause not in kb.clauses:
                    is_possible = False
            for clause in action.precond_neg:
                if clause in kb.clauses:
                    is_possible = False
            if is_possible:
                possible_actions.append(action)
        return possible_actions

    def result(self, state: str, action: Action):
        new_state = FluentState([], [])
        old_state = decode_state(state, self.state_map)
        for fluent in old_state.pos:
            if fluent not in action.effect_rem:
                new_state.pos.append(fluent)
        for fluent in action.effect_add:
            if fluent not in new_state.pos:
                new_state.pos.append(fluent)
        for fluent in old_state.neg:
            if fluent not in action.effect_add:
                new_state.neg.append(fluent)
        for fluent in action.effect_rem:
            if fluent not in new_state.neg:
                new_state.neg.append(fluent)
        return encode_state(new_state, self.state_map)

    def goal_test(self, state: str) -> bool:
        kb = PropKB()
        kb.tell(decode_state(state, self.state_map).pos_sentence())
        for clause in self.goal:
            if clause not in kb.clauses:
                return False
        return True

    def h_1(self, node: Node):
        # note that this is not a true heuristic
        h_const = 1
        return h_const

    @lru_cache(maxsize=8192)
    def h_pg_levelsum(self, node: Node):
        # uses the planning graph level-sum heuristic calculated
        # from this node to the goal
        # requires implementation in PlanningGraph
        pg = PlanningGraph(self, node.state)
        pg_levelsum = pg.h_levelsum()
        return pg_levelsum

    @lru_cache(maxsize=8192)
    def h_ignore_preconditions(self, node: Node):
        # not implemented
        count = 0
        return count
def dot_tree(problem):    
    """    pre : a Problem() as input    post: Dot graph in string format. Paste this in http://www.webgraphviz.com/    usage: print(dot_tree(problem))    """
    root = Node(problem.initial)    
    flatten = lambda l: [item for sublist in l for item in sublist]
    children=[root.child_node(problem, action) for action in problem.actions(root.state)]    
    grandchildren=flatten([[child.child_node(problem, action) for action in problem.actions(child.state)] for child in children])    
    greatgrandchildren=flatten([[child.child_node(problem, action) for action in problem.actions(child.state)] for child in grandchildren])    
    nodes=set(children+grandchildren+greatgrandchildren)
    import pydot    
    """    
    make a Dot graph of the nodes and connections    
    initial state as double circle     
    goal state is marked with thick lines    
    current implementation only goes two levels down (greatgrandchildren)    
    """            
    g = pydot.Dot()    
    g.set_type('digraph')    
    g.set_node_defaults(fontname = "helvetica",fontsize=10)    
    g.set_edge_defaults(fontname = "helvetica",fontsize=9)        
    g.add_node(pydot.Node(name=root.state,label='{}'.format(root.state),shape='doublecircle'))    
    for n in nodes:        
        if problem.goal_test(n.state):            
            penwidth=3        
        else:            
            penwidth=1                
        g.add_node(pydot.Node(name=n.state,label='{}'.format(n.state),penwidth=penwidth))    
    for n in nodes:
        g.add_edge(pydot.Edge(n.parent.state,n.state,label='{}'.format(n.action.name)))    
   return g.to_string()

def have_cake():
    def get_init():
        pos = [expr('Have(Cake)'),
               ]
        neg = [expr('Eaten(Cake)'),
               ]
        return FluentState(pos, neg)

    def get_goal():
        return [expr('Have(Cake)'),
                expr('Eaten(Cake)'),
                ]

    return HaveCakeProblem(get_init(), get_goal())


if __name__ == '__main__':
    p = have_cake()
    print("**** Have Cake example problem setup ****")
    print("Initial state for this problem is {}".format(p.initial))
    print("Actions for this domain are:")
    for a in p.actions_list:
        print('   {}{}'.format(a.name, a.args))
    print("Fluents in this problem are:")
    for f in p.state_map:
        print('   {}'.format(f))
    print("Goal requirement for this problem are:")
    for g in p.goal:
        print('   {}'.format(g))
    print()
    print("*** Breadth First Search")
    run_search(p, breadth_first_search)
    print("*** Depth First Search")
    run_search(p, depth_first_graph_search)
    print("*** Uniform Cost Search")
    run_search(p, uniform_cost_search)
    print("*** Greedy Best First Graph Search - null heuristic")
    run_search(p, greedy_best_first_graph_search, parameter=p.h_1)
    print("*** A-star null heuristic")
    run_search(p, astar_search, p.h_1)
    # print("A-star ignore preconditions heuristic")
    # rs(p, "astar_search - ignore preconditions heuristic", astar_search, p.h_ignore_preconditions)
    # print(""A-star levelsum heuristic)
    # rs(p, "astar_search - levelsum heuristic", astar_search, p.h_pg_levelsum)
