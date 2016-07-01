# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util
from game import Directions


class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def startingState(self):
    """
    Returns the start state for the search problem 
    """
    util.raiseNotDefined()

  def isGoal(self, state): #isGoal -> isGoal
    """
    state: Search state

    Returns True if and only if the state is a valid goal state
    """
    util.raiseNotDefined()

  def successorStates(self, state): #successorStates -> successorsOf
    """
    state: Search state
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
    """
    util.raiseNotDefined()

  def actionsCost(self, actions): #actionsCost -> actionsCost
    """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
    """
    util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def search(dataStructure,problem,problemType,heuristic=None):
  #Intitialize the problems starting state
  explored = set();
  if problemType == ucs or problemType == astar:
    dataStructure.push((problem.startingState(),[],0),0);
  else:
    dataStructure.push((problem.startingState(),[],0));

  #loop through our datastructure and pop the newest/oldest/lowest priority node
  #depending on what type of search we are performing
  while not dataStructure.isEmpty():
      # the node we pop from the dataStructure will be our parent node
      parentPostition, parentMoves, parentCost = dataStructure.pop();

      if parentPostition in explored: continue

      explored.add(parentPostition);

      #if we reach the goal node, return our list of moves
      if problem.isGoal(parentPostition): return parentMoves;

      #expand all the children of the parent node
      for childPosition, childMove, childCost in problem.successorStates(parentPostition):
        #depending on the type of problem, we will push the node onto the dataStructure with all
        #required properties
        if problemType == ucs:
          dataStructure.push((childPosition, parentMoves+[childMove], childCost), problem.actionsCost(parentMoves + [childMove]));
        elif problemType == astar:
          dataStructure.push((childPosition, parentMoves+[childMove], childCost), (problem.actionsCost(parentMoves + [childMove]) + heuristic(childPosition,problem)))
        else:
          dataStructure.push((childPosition, parentMoves+[childMove], childCost));

  # if we do not find the goal, return an empty set
  return [];

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:  
  print "Start:", problem.startingState()
  print "Is the start a goal?", problem.isGoal(problem.startingState())
  print "Start's successors:", problem.successorStates(problem.startingState())
  """
  return search(util.Stack(), problem,dfs)

def breadthFirstSearch(problem):
  return search(util.Queue(), problem,bfs)

  "Search the shallowest nodes in the search tree first. [p 81]"
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  return search(util.PriorityQueue(), problem, ucs)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  xy1 = problem
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def manhattanDistance( xy1, xy2 ):
  "Returns the Manhattan distance between points xy1 and xy2"
  return abs( xy1[0] - xy2[0] ) + abs( xy1[1] - xy2[1] )

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  return search(util.PriorityQueue(), problem, astar, heuristic)
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
