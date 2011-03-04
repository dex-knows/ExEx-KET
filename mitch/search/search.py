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

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
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

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"            

  from game import Directions 
  
  rootNode = problem.getStartState()
  frontier = [(rootNode, Directions.STOP, rootNode, 0)]
  frontierLocation=[rootNode]
  explored = []
  exploredLocation=[]

  while not len(frontier) == 0:
    newNode=frontier.pop()
    explored.append(newNode)
    exploredLocation.append(newNode[0])

    if problem.isGoalState(newNode[0]):return makeSolution(explored)
    successors = problem.getSuccessors(newNode[0])
    for successor in successors:
      if not((successor[0] in frontierLocation) & (successor[0] in exploredLocation)):
        frontier.append((successor[0], successor[1], newNode[0], successor[2]))
        frontierLocation.append(successor[0])
  return []

def makeSolution(explored):
  from game import Directions
  # The last step is for pacman to stop moving because he has reached his goal
  solution=[Directions.STOP]
  # We will initialize our search criteria to the goal node
  thisNode = explored.pop()
  parent = thisNode[0]
  # We need to return put the goal node back in so that it's direction can be added. This step is neccesary for the case when the goal node is the start node. In such a case the search will be skipped and only stop will be in the directions.
  explored.append(thisNode)
  # the 1st node will always be the start node, thus there are no directions to get there and should not be added the the solution.
  while len(explored)>1:
    thisNode = explored.pop()
    if thisNode[0] == parent:
      parent = thisNode[2]
      solution.append(thisNode[1])
  solution.reverse()
  return solution

"""
def DSrecurse(problem, actions, node):
  if problem.getSuccesors(node)
    if problem.isGoalState(node)
      return node[1]
"""

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  from game import Directions 
  
  rootNode = problem.getStartState()
  if problem.isGoalState(rootNode): return makeSolution(rootNode)
  frontier = [(rootNode, Directions.STOP, rootNode, 0)]
  frontierLocation=[rootNode]
  explored = []
  exploredLocation=[]

  while not len(frontier) == 0:
    newNode=frontier.pop()
    explored.append(newNode)
    exploredLocation.append(newNode[0])

    successors = problem.getSuccessors(newNode[0])
    for successor in successors:
      if problem.isGoalState(newNode[0]):return makeSolution(explored)
      if not((successor[0] in frontierLocation) & (successor[0] in exploredLocation)):
        frontier.insert(0, (successor[0], successor[1], newNode[0], successor[2]))
        frontierLocation.insert(0, successor[0])
  return []
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
