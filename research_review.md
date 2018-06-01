
### [AIND 2018 Term 1] Carl Wennstam - Research review

---
# Research review

[TOC]

- ##### Introduction
	- ###### Definitions of AI
	- ###### Practical use
	- ###### Choice of research papers
- ##### Planning in Games: An Overview and Lessons Learned
	- ###### Classical planning (STRIPS)
	- ###### Hierarchial Networks (HTN)
	- ###### Related techniques
	- ###### Utility systems	
	- ###### Lessons learned

 - ##### PDDL: A Language with a Purpose?


## Introduction
### Definitions of AI

Several definitions of AI exist, along two dimensions Thinking (Humanly vs Rationally) and Acting (Humanly vs Rationally). **Planning** seems to be a field of AI which fits well the two definitions given by our lecturers:
>AI is programming a computer to do the right thing *when you don't know what the right things is*. - **Peter Norvig**


This is the case in planning problems, as we are generating a behavior (which is generally on the Rationalist side but might be towards the Humanist side depending on the application) without knowing what that the optimal behavior will be.

>AI is clever solutions to exponential problems. - **Thad Starner**

This is also featured here, as we are dealing with employing **search** and **planning graphs** to **NP-hard** problems.


### Practical use
So, in theory, planning seems at the heart of AI. But how useful is it? With the recent hype around **neural networks** and **deep learning**, is planning (and planning graphs) still relevant? Some of my classmates did not seem convinced. 

#### Practical applications of shortest path algorithms
Consider a market for financial transactions that is based on trading commodities. The table in rates.txt shows conversion rates among currencies. The first line in the file is the number V of currencies; then the file has one line per currency, giving its name followed by the conversion rates to the other currencies. An arbitrage opportunity is a directed cycle such that the product of the exchange rates is greater than one. For example, our table says that 1,000 U.S. dollars will buy 1,000.00 × .741 = 741 euros, then we can buy 741 × 1.366 = 1,012.206 Canadian dollars with our euros, and finally, 1,012.206 × .995 = 1,007.14497 U.S. dollars with our Canadian dollars, a 7.14497-dollar profit! 

### Choice of research papers

- Planning in Games: Planning in Games: An Overview and Lessons Learned
	- Active industry applications
	- Discusses hiearical planning

- PDDL: A Language with a Purpose?
	- critique of PDDL usefullness in theoretical and practical terms
	- dfdf
	
- PDDL: A Language with a Purpose?
	- critique of PDDL usefullness in theoretical and practical terms
	- dfdf

## Planning in Games: An Overview and Lessons Learned
### Classical planning (STRIPS)
Classing planning, where we go from an initial state to a goal, requires a good definition of the problem so that A* can be applied. The first major game to apply this was F.E.A.R. in 2005. A planner was implemented to generate NPC behavior. This was feasible even 13 years ago due to the problems having short sequences. The game spawned a sequel, two expansions and inspired at least 5 other title.
One of the later iterations, Stalker (2008), added a nested structure so that more complex sequences could be generated out of the core STRIPS search.
### Hierarchial Networks (HTN)
HTN searches through actions that break down **recursively** using **task decomposition** and was first featured in Killzone 2, as the designers they wanted more control over the behaviors (approaching the Acting Humanly side). A **SHOP** (Simple Hierarchial Ordered Planner) turned out a big success, and allegedly the players were often suprised that the in-game bots were not in fact online players, thereby passing a type of **Turing test**. The later game Transformers : War for Cybertron used a similar **SHOP** algorithm which also tracked the (side)effects of all actions.

Generally, SHOP focuses on two core issues in planning:
For many types of planners, including HTN, their limitation is in the flexibility of the domain. Custom procedural functions can be hard to integrate when you don’t know how the planner may combine actions while planning. 
To deal with this, SHOP limits the expressiveness of the planner (by imposing an order on the plans) to make it easy to insert custom logic.

<p align="center"> 
<img src="images/shop.png">
</p>


### Related techniques
A **behavior tree** is similar to a HTN but stops at current action if "this is likely to work out", rather than searching the full graph. These have been in use in the industry since 2004, inspired by robotics and virtual agents from decades before.
A utility system is the term used to describe a voting/scoring system, and they are often applied to sub-systems of games like selecting objects/positions based on the results of a spread-sheet like calculation. Featured in **The Sims**.
 
#### Summary

The biggest open questions for using planners in game AI are about design, how to tweak the behaviors resulting from planners, and thinking more in terms of systems and emergent AIs. This has required significantly more effort than the pure algorithmic aspects of planning, and is responsible for the incremental transition towards hierarchical approaches.

In well understood domains, other techniques work best. In the cases of action/combat games, we can easily build robust AI that looks deliberate using simple reactive techniques like behavior trees. 

Planning has most benefits in **unknown domains**. One of the benefits of planning iss in prototyping, creating new behaviors quickly by letting the planner generate behavior given new actions or goals to work with. Planners also have shown to be more beneficial in open worlds, where the sandbox simulation has significantly more complexity.

Regardless of whether developers use planning techniques or not, an architecture that separates the AI's goals (or WHAT to do) and the AI's decision making (or HOW to do it), has proven to be very effective. Planning research has helped crystallize this insight, and even when using reactive techniques this is arguably a best practice for AI architecture in games today.

## Planning as Tabled Logic Programming

This paper describes Picat’s planner, its implementation, and planning models for several domains used in International Planning Competition (IPC) 2014. Picat’s planner is implemented by use of tabling. During search, every state encountered is tabled, and tabled states are used to eﬀectively perform resource-bounded search. In Picat, structured data can be used to avoid enumerating all possible permutations of objects, and term sharing is used to avoid duplication of common state data. This paper presents several modeling techniques through the example models, ranging from designing state representations to facilitate data sharing and symmetry breaking, encoding actions with operations for eﬃcient precondition checking and state updating, to incorporating domain knowledge and heuristics. Broadly, this paper demonstrates the eﬀectiveness of tabled logic programming for planning, and argues the importance of modeling despite recent signiﬁcant progress in domain-independent PDDL planners.


Tabling (Michie 1968; Tamaki and Sato 1986; Warren 1992) is a technique used in logic and functional programming systems, which caches the results of certain calculations in memory and reuses them in subsequent calculations through a quick table lookup. Like state marking used in search algorithms, tabling can prevent the same state from being expanded more than once during search. Tabling has been found useful in many search problems, including theorem proving (Nielson et al. 2004; Pientka 2003), program analysis (Dawson et al. 1996) and model checking (Ramakrishna et al. 1997). Recently, tabled logic programming has been successfully employed to solve speciﬁc planning problems (Bartak and Zhou 2014; Zhou and Dovier 2013; Zhou 2014), and has been shown to be

 As a modeling language for planning, Picat diﬀers from PDDL (Plan Domain Description Language) (McDermott 1998) and ASP (Brewka et al. 2011; Gebser et al. 2012; Lifschitz 2002) in several aspects: (1) Picat allows use of structures to represent states; (2) Picat supports explicit commitment and nondeterministic actions, which enables users to have better control over action applications; (3) Picat provides facilities for describing domain knowledge and heuristics for pruning search space. As a solving system, Picat’s planner implements several techniques for better performance. First, it tables every state encountered during search and avoids repeating the exploration of the same state. Second, it adopts the hash-consing technique (Zhou and Have 2012) to share common state data and to speed up the equality testing of states. Third, it utilizes tabled states to eﬀectively perform resource-bounded search. For optimal planning, Picat oﬀers built-ins to perform iterative search, but unlike IDA* (Korf 1985), Picat also reuses results tabled in early iterations (Zhou 2014). This paper shows that the above-mentioned features of Picat make Picat a more appropriate language than PDDL for modeling and solving planning problems. To that end, this paper presents examples in Picat for several domains used in IPC’14. These examples illustrate several modeling techniques on how to design state representations to facilitate data sharing and symmetry breaking, on how to translate PDDL operators into Picat actions, and on how to incorporate domain knowledge and heuristics to reduce search spaces. This paper also gives the experimental results of the presented models and several other models encoded in the same way. The experimental results demonstrate the eﬀectiveness of tabling and the importance of modeling.


## PDDL: A Language with a Purpose?


### References

- *Planning in Games: An Overview and Lessons Learned*, **Alex J. CHAMPANDARD**, AiGameDev.com (March, 2013) http://aigamedev.com/open/review/planning-in-games/

- *PDDL: A Language with a Purpose?*, **T. L. MCCLUSKEY**, Department of Computing and Mathematical Science, School of Computing and Engineering,University of Huddersfield, UK (June, 2003)

- *Planning as Tabled Logic Programming*, **N-F. ZHOU**, CUNY Brooklyn College and Graduation Center (July, 2015)   https://arxiv.org/pdf/1507.03979.pdf








https://arxiv.org/pdf/1306.4040.pdf



https://arxiv.org/pdf/1106.0230v1.pdf


   [1]: http://aigamedev.com/open/review/planning-in-games/ "Planning in Games"
   [2]: https://algs4.cs.princeton.edu/44sp/ "FX Arbitrage"
   [3]: University of Huddersfield, UK, https://algs4.cs.princeton.edu/44sp/ "PDDL: A Language with a Purpose?"


You can also put the [link URL][1] below the current paragraph
like [this][2].

   [1]: http://aigamedev.com/open/review/planning-in-games/ "Planning in Games"
   [2]: https://algs4.cs.princeton.edu/44sp/ "FX Arbitrage"
   [3]: https://algs4.cs.princeton.edu/44sp/ "PDDL: A Language with a Purpose?"



## Environment requirements
- Python 3.4 or higher
- Starter code includes a copy of [companion code](https://github.com/aimacode) from the Stuart Russel/Norvig AIMA text.  


"Artificial Intelligence: A Modern Approach" 3rd edition chapter 10 *or* 2nd edition Chapter 11 on Planning, available [on the AIMA book site](http://aima.cs.berkeley.edu/2nd-ed/newchap11.pdf) sections: 

- *The Planning Problem*
- *Planning with State-space Search*

- Air Cargo Action Schema:
```
Action(Load(c, p, a),
	PRECOND: At(c, a) ∧ At(p, a) ∧ Cargo(c) ∧ Plane(p) ∧ Airport(a)
	EFFECT: ¬ At(c, a) ∧ In(c, p))
Action(Unload(c, p, a),
	PRECOND: In(c, p) ∧ At(p, a) ∧ Cargo(c) ∧ Plane(p) ∧ Airport(a)
	EFFECT: At(c, a) ∧ ¬ In(c, p))
Action(Fly(p, from, to),
	PRECOND: At(p, from) ∧ Plane(p) ∧ Airport(from) ∧ Airport(to)
	EFFECT: ¬ At(p, from) ∧ At(p, to))
```

- Problem 1 initial state and goal:
```
Init(At(C1, SFO) ∧ At(C2, JFK) 
	∧ At(P1, SFO) ∧ At(P2, JFK) 
	∧ Cargo(C1) ∧ Cargo(C2) 
	∧ Plane(P1) ∧ Plane(P2)
	∧ Airport(JFK) ∧ Airport(SFO))
Goal(At(C1, JFK) ∧ At(C2, SFO))
```
- Problem 2 initial state and goal:
```
Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) 
	∧ At(P1, SFO) ∧ At(P2, JFK) ∧ At(P3, ATL) 
	∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3)
	∧ Plane(P1) ∧ Plane(P2) ∧ Plane(P3)
	∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL))
Goal(At(C1, JFK) ∧ At(C2, SFO) ∧ At(C3, SFO))
```
- Problem 3 initial state and goal:
```
Init(At(C1, SFO) ∧ At(C2, JFK) ∧ At(C3, ATL) ∧ At(C4, ORD) 
	∧ At(P1, SFO) ∧ At(P2, JFK) 
	∧ Cargo(C1) ∧ Cargo(C2) ∧ Cargo(C3) ∧ Cargo(C4)
	∧ Plane(P1) ∧ Plane(P2)
	∧ Airport(JFK) ∧ Airport(SFO) ∧ Airport(ATL) ∧ Airport(ORD))
Goal(At(C1, JFK) ∧ At(C3, JFK) ∧ At(C2, SFO) ∧ At(C4, SFO))
```



#### TODO: Experiment and document metrics for non-heuristic planning solution searches
* Run uninformed planning searches for `air_cargo_p1`, `air_cargo_p2`, and `air_cargo_p3`; provide metrics on number of node expansions required, number of goal tests, time elapsed, and optimality of solution for each search algorithm. Include the result of at least three of these searches, including breadth-first and depth-first, in your write-up (`breadth_first_search` and `depth_first_graph_search`). 
* If depth-first takes longer than 10 minutes for Problem 3 on your system, stop the search and provide this information in your report.
* Use the `run_search` script for your data collection: from the command line type `python run_search.py -h` to learn more.

>#### Why are we setting the problems up this way?  
>Progression planning problems can be 
solved with graph searches such as breadth-first, depth-first, and A*, where the 
nodes of the graph are "states" and edges are "actions".  A "state" is the logical 
conjunction of all boolean ground "fluents", or state variables, that are possible 
for the problem using Propositional Logic. For example, we might have a problem to 
plan the transport of one cargo, C1, on a
single available plane, P1, from one airport to another, SFO to JFK.
![state space](images/statespace.png)
In this simple example, there are five fluents, or state variables, which means our state 
space could be as large as ![2to5](images/twotofive.png). Note the following:
>- While the initial state defines every fluent explicitly, in this case mapped to **TTFFF**, the goal may 
be a set of states.  Any state that is `True` for the fluent `At(C1,JFK)` meets the goal.
>- Even though PDDL uses variable to describe actions as "action schema", these problems
are not solved with First Order Logic.  They are solved with Propositional logic and must
therefore be defined with concrete (non-variable) actions
and literal (non-variable) fluents in state descriptions.
>- The fluents here are mapped to a simple string representing the boolean value of each fluent
in the system, e.g. **TTFFTT...TTF**.  This will be the state representation in 
the `AirCargoProblem` class and is compatible with the `Node` and `Problem` 
classes, and the search methods in the AIMA library.  


### Part 2 - Domain-independent heuristics
#### READ: Stuart Russel and Peter Norvig text
"Artificial Intelligence: A Modern Approach" 3rd edition chapter 10 *or* 2nd edition Chapter 11 on Planning, available [on the AIMA book site](http://aima.cs.berkeley.edu/2nd-ed/newchap11.pdf) section: 

- *Planning Graph*

#### TODO: Implement heuristic method in `my_air_cargo_problems.py`
- `AirCargoProblem.h_ignore_preconditions` method

#### TODO: Implement a Planning Graph with automatic heuristics in `my_planning_graph.py`
- `PlanningGraph.add_action_level` method
- `PlanningGraph.add_literal_level` method
- `PlanningGraph.inconsistent_effects_mutex` method
- `PlanningGraph.interference_mutex` method
- `PlanningGraph.competing_needs_mutex` method
- `PlanningGraph.negation_mutex` method
- `PlanningGraph.inconsistent_support_mutex` method
- `PlanningGraph.h_levelsum` method


#### TODO: Experiment and document: metrics of A* searches with these heuristics
* Run A* planning searches using the heuristics you have implemented on `air_cargo_p1`, `air_cargo_p2` and `air_cargo_p3`. Provide metrics on number of node expansions required, number of goal tests, time elapsed, and optimality of solution for each search algorithm and include the results in your report. 
* Use the `run_search` script for this purpose: from the command line type `python run_search.py -h` to learn more.

>#### Why a Planning Graph?
>The planning graph is somewhat complex, but is useful in planning because it is a polynomial-size approximation of the exponential tree that represents all possible paths. The planning graph can be used to provide automated admissible heuristics for any domain.  It can also be used as the first step in implementing GRAPHPLAN, a direct planning algorithm that you may wish to learn more about on your own (but we will not address it here).

>*Planning Graph example from the AIMA book*
>![Planning Graph](images/eatcake-graphplan2.png)

### Part 3: Written Analysis
#### TODO: Include the following in your written analysis.  
- Provide an optimal plan for Problems 1, 2, and 3.
- Compare and contrast non-heuristic search result metrics (optimality, time elapsed, number of node expansions) for Problems 1,2, and 3. Include breadth-first, depth-first, and at least one other uninformed non-heuristic search in your comparison; Your third choice of non-heuristic search may be skipped for Problem 3 if it takes longer than 10 minutes to run, but a note in this case should be included.
- Compare and contrast heuristic search result metrics using A* with the "ignore preconditions" and "level-sum" heuristics for Problems 1, 2, and 3.
- What was the best heuristic used in these problems?  Was it better than non-heuristic search planning methods for all problems?  Why or why not?
- Provide tables or other visual aids as needed for clarity in your discussion.

## Examples and Testing:
- The planning problem for the "Have Cake and Eat it Too" problem in the book has been
implemented in the `example_have_cake` module as an example.
- The `tests` directory includes `unittest` test cases to evaluate your implementations. All tests should pass before you submit your project for review. From the AIND-Planning directory command line:
    - `python -m unittest tests.test_my_air_cargo_problems`
    - `python -m unittest tests.test_my_planning_graph`
    - You can run all the test cases with additional context by running `python -m unittest -v`
- The `run_search` script is provided for gathering metrics for various search methods on any or all of the problems and should be used for this purpose.

## Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named cargo_planning-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

## Improving Execution Time

The exercises in this project can take a *long* time to run (from several seconds to a several hours) depending on the heuristics and search algorithms you choose, as well as the efficiency of your own code.  (You may want to stop and profile your code if runtimes stretch past a few minutes.) One option to improve execution time is to try installing and using [pypy3](http://pypy.org/download.html) -- a python JIT, which can accelerate execution time substantially.  Using pypy is *not* required (and thus not officially supported) -- an efficient solution to this project runs in very reasonable time on modest hardware -- but working with pypy may allow students to explore more sophisticated problems than the examples included in the project.
