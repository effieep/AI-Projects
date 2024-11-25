# multiAgents.py
# --------------
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


from ast import Is
from math import exp
import re
from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        "*** YOUR CODE HERE ***"
        # Initialize the score with the base score of the successor state
        score = successorGameState.getScore()

        # Avoid ghosts that are not scared
        for i, ghostState in enumerate(newGhostStates):
            position = ghostState.getPosition()
            distance = manhattanDistance(newPos, position)
            if distance > 0:
                score -= 25.0 / distance
        
        # Encourage moving towards food
        if newFood:
            closestFood = min(manhattanDistance(newPos, food) for food in newFood)
            if closestFood > 0:
                score += 15.0 / closestFood 

        # The smaller the number of food pellets, the higher the score
        score -= len(newFood) * 5  # A penalty of 5 points for each remaining food pellet
    
        return score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        return self.max_value(gameState, depth)[1]
        util.raiseNotDefined()
    
    def min_value(self, gameState: GameState, depth: int, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        
        minv= float('inf')
        min_action = Directions.STOP

        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)

            value = 0
            # if we reached the total number of agents, it is the turn of pacman
            if a == gameState.getNumAgents() - 1:  
                value = self.max_value(successor, depth + 1)[0]
            # if it is the turn of a ghost, get the min value from the next ghost
            else:
                # if it is the turn of a ghost, get the min value from the next ghost
                value = self.min_value(successor, depth, a + 1)[0]
            
            # Update the min value and action
            if value < minv:
                minv = value
                min_action = action
        return minv, min_action

    def max_value(self, gameState: GameState, depth: int, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        maxv= float('-inf')
        max_action = Directions.STOP

        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)
            # Call min_value for the next agent
            value = self.min_value(successor, depth, 1)[0]
            # Update the max value and action
            if value > maxv:
                maxv = value
                max_action = action
        
        return maxv, max_action
    


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        depth = 0
        return self.max_value_ab(gameState, depth, float('-inf'), float('inf'))[1]
        util.raiseNotDefined()


    def min_value_ab(self, gameState: GameState, depth: int, alpha: float, beta: float, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP

        minv= float('inf')
        min_action = Directions.STOP

        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)

            value = 0
            # if we reached the total number of agents, it is the turn of pacman
            if a == gameState.getNumAgents() - 1:  
                value = self.max_value_ab(successor, depth + 1, alpha, beta)[0]
            else:
                # if it is the turn of a ghost, get the min value from the next ghost
                value = self.min_value_ab(successor, depth, alpha, beta,a + 1)[0]
            
            if value < minv:
                minv = value
                min_action = action

            if value < alpha:
                return value, action
            beta = min(beta, value)
        return minv, min_action

    def max_value_ab(self, gameState: GameState, depth: int, alpha: float, beta: float, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        
        maxv= float('-inf')
        max_action = Directions.STOP

        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)
            value = self.min_value_ab(successor, depth, alpha, beta, 1)[0]
            if value > maxv:
                maxv = value
                max_action = action
            if value > beta:
                return value, action
            alpha = max(alpha, value)
        return maxv, max_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """

        depth = 0
        return self.max_value(gameState, depth)[1]
        util.raiseNotDefined()

    def expect_value(self, gameState: GameState, depth: int, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
        
        min_action = Directions.STOP
        total_value = 0
        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)
            # if we reached the total number of agents, it is the turn of pacman
            if a == gameState.getNumAgents() - 1:  
                value = self.max_value(successor, depth + 1)[0]
            else:
                # if it is the turn of a ghost, get the expect value from the next ghost
                value = self.expect_value(successor, depth, a + 1)[0]
            
            total_value += value
        # Calculate the expected value, average of the values
        expected_value = total_value / len(gameState.getLegalActions(a))
        return expected_value, min_action
        

    def max_value(self, gameState: GameState, depth: int, a = 0):
        if depth >= self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP
 
        maxv= float('-inf')
        max_action = Directions.STOP

        for action in gameState.getLegalActions(a):
            successor = gameState.generateSuccessor(a, action)
            # Call expect_value for the next agent
            value = self.expect_value(successor, depth, 1)[0]
            if value > maxv:
                maxv = value
                max_action = action
        
        return maxv, max_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This function evaluates the current state and NOT the successor state based on an action.
    Encouraging Pac-Man to eat food and capsules.
    Prioritizing chasing scared ghosts for extra points.
    Avoiding active ghosts to reduce the risk of losing the game.
    Minimizing the number of food pellets left on the board.
    """
    # Extract features
    pacman_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    # Food and capsule distances
    if not food_list:
        food_distance = 1
    else:
        food_distance = min([manhattanDistance(pacman_pos, food) for food in food_list])

    if not capsules:
        capsule_distance = 1
    else:
        capsule_distance = min([manhattanDistance(pacman_pos, cap) for cap in capsules])
    
    ghost_penalty = 0
    scared_ghost_reward = 0
    
    # Evaluate ghost proximity
    for ghost in ghost_states:
        ghost_distance = manhattanDistance(pacman_pos, ghost.getPosition())
        isScared = ghost.scaredTimer > 0
        if isScared:
            scared_ghost_reward += max(15 - ghost_distance, 0) 
        else:
            if ghost_distance <= 2 and ghost_distance > 0:
                # Penalty applied for being too close to a ghost
                ghost_penalty -= 40/ghost_distance

    # Penalty for remaining food
    remaining_food_penalty = - (len(food_list) * 20)
    
    # Evaluation final score
    evaluation_score = (score + 20 / food_distance  + 20 / capsule_distance  + scared_ghost_reward + ghost_penalty  + remaining_food_penalty)
    return evaluation_score
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction