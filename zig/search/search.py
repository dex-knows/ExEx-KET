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

class Node(object):
    """Basic representation of a node on a map/tree.
       """
    def __init__(self, value, parent=None):
        """Value is exepected to be a triple with the following parts:
            1. Coordinate tuple (x,y)
            2. Direction string (e.g. "west)
            3. Path cost as an integer (e.g. 1)
        Parent is a coordinate.
           """
        self.coordinate = value[0]
        self.direction = value[1]
        self.cost = value[2]
        self.parent = parent

class NodeImproved(object):
    """Basic representation of a node on a map/tree.
       """
    def __init__(self, coordinate, accum_cost=0, accum_directions=[]):
        """
           """
        self.coordinate = coordinate 
        self.accumalitive_cost = accum_cost #Integer of cost up to this point
        self.accumalitive_directions = accum_directions # list of directions

def depthFirstSearch(problem):
    """A hackish DFS algorithm specific to solving single-destination problems.
       """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    starting_position = problem.getStartState()
    current_node = Node((starting_position, "", 0)) 
    
    all_nodes = [starting_position]    # List of coordinates
    fringe_nodes = []                  # List of nodes (we need to know its' parent)
    current_path = [current_node]      # List of coordinates 
    solution = []                      # List of directions from game module

    while not problem.isGoalState(current_node.coordinate):
        for successor in problem.getSuccessors(current_node.coordinate):
            # Prevent loops by only adding new nodes
            if successor[0] not in all_nodes:
                all_nodes.append(successor[0])
                fringe_nodes.append(Node(successor, current_node.coordinate))

        next_node = fringe_nodes.pop()

        # if the next fringe node is not a child of the last node in our path...
        if not next_node.parent == current_path[-1].coordinate:
            # Pop nodes off our current path until it has the next_node as a child 
            while next_node.parent != current_path[-1].coordinate:
                current_path.pop()  

        # Add it to our path and continue descending the tree.
        current_path.append(next_node) 
        current_node = next_node

    if not problem.isGoalState(current_node.coordinate):
        print "Failed to find a path to the goal state..."
    else:
        # Take our curren_path and turn it into a list of directions 
        last_coordinate = starting_position
        for node in current_path:
            if node.coordinate != starting_position:
                direction = node.direction
                if   direction == "West":
                    solution.append(w)
                elif direction == "South":
                    solution.append(s)
                elif direction == "North":
                    solution.append(n)
                elif direction == "East":
                    solution.append(e)
    return solution   
        
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
       """
    util.raiseNotDefined()

def translate_directions(path):
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH
    
    solution = []
    for direction in path:
        if direction == "West":
           solution.append(w)
        elif direction == "South":
           solution.append(s)
        elif direction == "North":
           solution.append(n)
        elif direction == "East":
           solution.append(e)
           
    return solution

def manhattanHeuristic(coordinate, problem):
  xy1 = coordinate
  xy2 = problem.goal
  return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
      
def uniformCostSearch(problem):
    """Search the node of least total cost first. 
       """
    # Bootstap...
    starting_position = problem.getStartState()
    root_node = NodeImproved(starting_position) 
    fringe = [root_node]
    all_nodes = [] # prevent loops

    # Main loop...
    while(True):
        fringe = sorted(fringe, key=lambda node: node.accumalitive_cost, reverse=True)
        node_to_expand = fringe.pop()
        accum_cost = node_to_expand.accumalitive_cost
        accum_directions = node_to_expand.accumalitive_directions

        for child in problem.getSuccessors(node_to_expand.coordinate):
            if child[0] not in all_nodes:
              all_nodes.append(child[0])
              new_cost = accum_cost + child[2]
              new_directions = accum_directions[:]
              new_directions.append(child[1])
              new_node = NodeImproved(child[0], new_cost, new_directions) 
              fringe.append(new_node)
        
        if problem.isGoalState(node_to_expand.coordinate):
            return translate_directions(node_to_expand.accumalitive_directions)

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
       """
    # Bootstap...
    starting_position = problem.getStartState()
    root_node = NodeImproved(starting_position) 
    fringe = [root_node]
    all_nodes = [] # prevent loops

    # Main loop...
    while(True):
        fringe = sorted(fringe, key=lambda node: manhattanHeuristic(node.coordinate, problem) + node.accumalitive_cost, reverse=True)
        node_to_expand = fringe.pop()
        accum_cost = node_to_expand.accumalitive_cost
        accum_directions = node_to_expand.accumalitive_directions

        for child in problem.getSuccessors(node_to_expand.coordinate):
            if child[0] not in all_nodes:
              all_nodes.append(child[0])
              new_cost = accum_cost + child[2]
              new_directions = accum_directions[:]
              new_directions.append(child[1])
              new_node = NodeImproved(child[0], new_cost, new_directions) 
              fringe.append(new_node)
        
        if problem.isGoalState(node_to_expand.coordinate):
            return translate_directions(node_to_expand.accumalitive_directions)
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
