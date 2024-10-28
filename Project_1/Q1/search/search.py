# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions
from typing import List

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.
    """
    # Stack to store (node, path) pairs - LIFO
    frontier = util.Stack()
    #Add the start state to the stack
    frontier.push((problem.getStartState(), []))  
    # Set to keep track of visited nodes
    expanded = set() 
    while not frontier.isEmpty():
        node, path = frontier.pop()  
        # print(node,path)
        # Check if the node is the goal
        if problem.isGoalState(node):
            return path 

        # Skip nodes that have already been visited
        if node in expanded:
            continue

        expanded.add(node)

        # Get successors of the current node
        for successor, action, stepCost in problem.getSuccessors(node):
            if successor not in expanded:
                # Add successor to the stack with the updated path
                new_path = path + [action]  
                frontier.push((successor, new_path))
                
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # Queue to store (node, path) pairs - FIFO
    frontier = util.Queue()
    #Add the start state to the stack
    frontier.push((problem.getStartState(), [])) 
    # Set to keep track of visited nodes
    expanded = set() 
    while not frontier.isEmpty():
        node, path = frontier.pop() 
        # Check if the node is the goal
        if problem.isGoalState(node):
            return path  

        # Skip nodes that have already been visited
        if node in expanded:
            continue

        expanded.add(node)

        # Get successors of the current node
        for successor, action, stepCost in problem.getSuccessors(node):
            if successor not in expanded:
                # Add successor to the stack with the updated path
                new_path = path + [action]  
                frontier.push((successor, new_path))
                
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Priority queue to store (node, path, path cost) pairs
    # Each time extracts the node with the lowest path cost
    frontier = util.PriorityQueue()
    #Add the start state to the priority queue
    frontier.push((problem.getStartState(), [],0),problem.getCostOfActions([]))  
    # Set to keep track of visited nodes
    expanded = set() 
    while not frontier.isEmpty():
        node, path, path_cost = frontier.pop()  
        # print(node,path,path_cost)
        # Check if the node is the goal
        if problem.isGoalState(node):
            return path 

        # Skip nodes that have already been visited
        if node in expanded:
            continue

        expanded.add(node)

        # Get successors of the current node
        for successor, action, stepCost in problem.getSuccessors(node):
            if successor not in expanded:
                # Add successor to the stack with the updated path
                new_path = path + [action]  
                cost = problem.getCostOfActions(new_path)
                frontier.push((successor, new_path,cost),cost)
                
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # Priority queue to store (node, path, path cost) pairs
    # Each time extracts the node with the lowest priority, path_cost + heuristic
    frontier = util.PriorityQueue()
    #Add the start state to the priority queue
    frontier.push((problem.getStartState(), [],0),heuristic(problem.getStartState(),problem) + problem.getCostOfActions([]))

    # Keep track of the best cost to reach each node
    best_cost = {problem.getStartState(): 0}
    
    while not frontier.isEmpty():
        current_state, path, path_cost = frontier.pop()

        # If this is the goal state, return the path
        if problem.isGoalState(current_state):
            return path

        # Get successors of the current node
        for successor, action, stepCost in problem.getSuccessors(current_state):
            # Calculate the new path and cost to reach the successor
            new_path = path + [action]
            new_cost = path_cost + stepCost

            # If the new cost to reach the successor is lower than any previously found cost, update best_cost
            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost  # Update best cost for the successor

                # Calculate priority as the sum of the cost and the heuristic
                priority = new_cost + heuristic(successor, problem)

                # Add successor to the priority queue
                frontier.push((successor, new_path, new_cost), priority)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
