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
  
  """
  print "Start:", problem.getStartState()
  print "Goal:", problem.goal
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  
  print "(3,3)'s successors:", problem.getSuccessors((3,3))[:][0]
  """
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  n = Directions.NORTH
  e = Directions.EAST
  """  
  global goal
  
  def dfs(graph, node, visited, parents):
    if problem.isGoalState(node):
        global goal
        goal = node
        #print "++++"
        return visited, parents
    if node not in visited:
        visited.append(node)
        #print node, visited, problem.getSuccessors(node)
        for n in problem.getSuccessors(node):
            if n[0] not in parents:
                parents[n[0]] = node 
            # print node, n, parents
            dfs(graph,n[0], visited, parents)
    return visited, parents

  parents = {problem.getStartState():0}
  visited, parents = dfs(problem, problem.getStartState(), [], parents)
  
  path = []

  #print visited
  #print parents
  
  "reconstruction of the path"
  curr = goal
  while (parents[curr] != 0):
      previous = parents[curr]
      #print curr, previous
      for successor in problem.getSuccessors(previous):
          if successor[0] == curr:
              path = [successor[1]] + path
      curr = previous
  #print path
      
  return path


  #util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  "*** YOUR CODE HERE ***"
  
  """
  parents = {problem.getStartState():0}
  visited = []
  
  to_explore = util.Queue()
  to_explore.push(problem.getStartState())
  
  path = []
  
  while not to_explore.isEmpty():
      node = to_explore.pop()
      if problem.isGoalState(node):
          goal = node
          break
      if node not in visited:
          visited.append(node)
          #print node, visited, problem.getSuccessors(node)
      for n in problem.getSuccessors(node):
          if n[0] not in visited:
              to_explore.push(n[0])
          if n[0] not in parents:
              parents[n[0]] = node 
              # print node, n, parents

  #print visited
  #print parents
  
  "reconstruction of the path"
  curr = goal
  while (parents[curr] != 0):
      previous = parents[curr]
      #print curr, previous
      for successor in problem.getSuccessors(previous):
          if successor[0] == curr:
              path = [successor[1]] + path
      curr = previous
  #print path
      
  return path
  """
  "https://github.com/weixsong/pacman/blob/master/search.py"
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  print problem

  frontier = util.Queue()
  visited = dict()

  state = problem.getStartState()
  node = {}
  node["parent"] = None
  node["action"] = None
  node["state"] = state
  frontier.push(node)

  while not frontier.isEmpty():
    node = frontier.pop()
    state = node["state"]
    if visited.has_key(state):
      continue

    visited[state] = True
    if problem.isGoalState(state) == True:
      break

    for child in problem.getSuccessors(state):
      if child[0] not in visited:
        sub_node = {}
        sub_node["parent"] = node
        sub_node["state"] = child[0]
        sub_node["action"] = child[1]
        frontier.push(sub_node)

  actions = []
  while node["action"] != None:
    actions.insert(0, node["action"])
    node = node["parent"]

  return actions

  
  
  #util.raiseNotDefined()
      
def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  
  global goal
  
  parents = {problem.getStartState():0}
  visited = []
  
  to_explore = util.PriorityQueue()
  to_explore.push(problem.getStartState(),0)
  
  path = []
  
  while not to_explore.isEmpty():
      node = to_explore.pop()
      if problem.isGoalState(node):
          global goal
          goal = node
          break
      if node not in visited:
          visited.append(node)
          #print node, visited, problem.getSuccessors(node)
      for n in problem.getSuccessors(node):
          if n[0] not in visited:
              to_explore.push(n[0],n[2])
          if n[0] not in parents:
              parents[n[0]] = node 
              # print node, n, parents

  #print visited
  #print parents
  
  "reconstruction of the path"
  curr = goal
  while (parents[curr] != 0):
      previous = parents[curr]
      #print curr, previous
      for successor in problem.getSuccessors(previous):
          if successor[0] == curr:
              path = [successor[1]] + path
      curr = previous
  #print path
      
  return path
  
  #util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  """
  global goal
  
  parents = {problem.getStartState():0}
  visited = []
  
  to_explore = util.PriorityQueue()
  to_explore.push(problem.getStartState(),0)
  
  path = []
  
  while not to_explore.isEmpty():
      node = to_explore.pop()
      if problem.isGoalState(node):
          global goal
          goal = node
          break
      if node not in visited:
          visited.append(node)
          #print node, visited, problem.getSuccessors(node)
      for n in problem.getSuccessors(node):
          if n[0] not in visited:
              to_explore.push(n[0],n[2] + heuristic(n[0],problem))
          if n[0] not in parents:
              parents[n[0]] = node 
              # print node, n, parents

  #print visited
  #print parents
  
  "reconstruction of the path"
  curr = goal
  while (parents[curr] != 0):
      previous = parents[curr]
      #print curr, previous
      for successor in problem.getSuccessors(previous):
          if successor[0] == curr:
              path = [successor[1]] + path
      curr = previous
  #print path
      
  return path
  """
  
  "https://github.com/weixsong/pacman/blob/master/search.py"
  #print "Start:", problem.getStartState()
  #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  #print "Start's successors:", problem.getSuccessors(problem.getStartState())
  #print problem

  frontier = util.PriorityQueue()
  visited = dict()

  state = problem.getStartState()
  #print "state", state
  node = {}
  node["parent"] = None
  node["action"] = None
  node["state"] = state
  node["cost"] = 0
  node["eval"] = heuristic(state, problem)
  frontier.push(node, node["cost"] + node["eval"])

  while not frontier.isEmpty():
    node = frontier.pop()
    state = node["state"]
    cost = node["cost"]
    v = node["eval"]
    if visited.has_key(state):
      continue
    visited[state] = True
    
    if problem.isGoalState(state) == True:
      break

    for child in problem.getSuccessors(state):
      if child[0] not in visited:
        sub_node = {}
        sub_node["parent"] = node
        sub_node["state"] = child[0]
        sub_node["action"] = child[1]
        sub_node["cost"] = child[2] + cost
        sub_node["eval"] = heuristic(sub_node["state"], problem)
        frontier.push(sub_node, sub_node["cost"] + node["eval"])

  actions = []
  while node["action"] != None:
    actions.insert(0, node["action"])
    node = node["parent"]

  return actions
  
  #util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
