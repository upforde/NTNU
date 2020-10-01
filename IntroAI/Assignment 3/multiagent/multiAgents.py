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

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
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

    def evaluationFunction(self, currentGameState, action):
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
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
    # This section has been changed from the original multiAgents.py
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.
        """

        def minimax(state, depth, agent):
            """
            Function minimax takes in the current state of the game, the desired max depth
            and the agent to get the minimax action for as parameters and runs recursively
            to return the value of the move as well as the minimax action.
            """
            # Check if max depth or a terminal state has been reached
            if depth == self.depth or state.isWin() or state.isLose():
                # then the function returns the value of the current state
                # it also returns None as the best move to take, because it has reached
                # a terminal point or the farthest depth, meaning there aren't anymore
                # moves to take
                return self.evaluationFunction(state), None

            # Checks what kind of agent it is. 
            # If it's pac-man
            if agent == 0:
                # Initiate the value to be -infinity and the best move to be None
                v, bestMove = float('-inf'), None
                # For each move that pac-man can take
                for action in state.getLegalActions(agent):
                    # check the value of the state that this action will take pac-man to
                    evaluation = minimax(state.generateSuccessor(agent, action), depth, 1)[0]
                    # if the evaluated value of the current action is greater than
                    # the current highest value
                    if v < evaluation:
                        # then the current highest value gets set to the value of the current action 
                        # and the best move is set to be the current action
                        v, bestMove = evaluation, action
                # The function returns the highest value and the best move to take
                return v, bestMove
            # If the agens is a ghost
            else:
                # Initiate the value to be infinity and the best move to be None
                v, bestMove = float('inf'), None
                # For each move that a ghost can take
                for action in state.getLegalActions(agent):
                    # checking wether the next agent is a ghost or not
                    nextAgent = agent+1 if agent+1 < state.getNumAgents() else 0
                    # check wether the depth will increment or not
                    nextDepth = depth+1 if nextAgent == 0 else depth
                    # check the value of the state that this action will take the ghost to
                    evaluation = minimax(state.generateSuccessor(agent, action), nextDepth, nextAgent)[0]
                    # if the evaluated value of the current action is lower than 
                    # the current lowest value
                    if v > evaluation:
                        # then the current lowest value gets set to the value of the current action 
                        # and the best move is set to be the current action
                        v, bestMove = evaluation, action
                # The function returns the lowest value and the best move to take
                return v, bestMove
        
        # The getAction function runs the minimax function and returns the best action to take
        return minimax(gameState, 0, 0)[1]



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    # This section has been changed from the original multiAgents.py
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """

        def alphaBeta(state, depth, agent, alpha=float('-inf'), beta=float('inf')):
            """
            Function alphaBeta takes in the current state of the game, the desired max depth
            and the agent to get the alphaBeta pruned minimax action for as parameters. It allso takes in optional
            parameters for alpha and beta, which are used to see if a tree branch should be pruned or not.
            The function runs recursively to return the value of the move as well as the alphaBeta pruned minimax action.
            """

            # Check if max depth or a terminal state has been reached
            if depth == self.depth or state.isWin() or state.isLose():
                # then the function returns the value of the current state
                # it also returns None as the best move to take, because it has reached
                # a terminal point or the farthest depth, meaning there aren't anymore
                # moves to take
                return self.evaluationFunction(state), None

            # Checks what kind of agent it is. 
            # If it's pac-man
            if agent == 0:
                # Initiate the value to be -infinity and the best move to be None
                v, bestMove = float('-inf'), None
                # For each move that pac-man can take
                for action in state.getLegalActions(agent):
                    # check the value of the state that this action will take pac-man to
                    evaluation = alphaBeta(state.generateSuccessor(agent, action), depth, 1, alpha, beta)[0]
                    # if the evaluated value of the current action is greater than
                    # the current highest value
                    if v < evaluation:
                        # then the current highest value gets set to the value of the current action 
                        # and the best move is set to be the current action
                        v, bestMove = evaluation, action
                    # setting alpha to be the biggest between alpha and evaluation
                    alpha = max(evaluation, alpha)
                    # if alpha is bigger than beta, then break out of the recursion and effectively prune this branch
                    if alpha > beta: break
                # The function returns the highest value and the best move to take
                return v, bestMove

            # If the agens is a ghost
            else:
                # Initiate the value to be infinity
                v = float('inf')
                # Initiate the best move to be None
                bestMove = None
                # For each move that a ghost can take
                for action in state.getLegalActions(agent):
                    # checking wether the next agent is a ghost or not
                    nextAgent = agent+1 if agent+1 < state.getNumAgents() else 0
                    # check wether the depth will increment or not
                    nextDepth = depth+1 if nextAgent == 0 else depth
                    # check the value of the state that this action will take the ghost to
                    evaluation = alphaBeta(state.generateSuccessor(agent, action), nextDepth, nextAgent, alpha, beta)[0]
                    # if the evaluated value of the current action is lower than 
                    # the current lowest value
                    if v > evaluation:
                        # then the current lowest value gets set to the value of the current action 
                        # and the best move is set to be the current action
                        v, bestMove = evaluation, action
                    # setting beta to be the smallest between beta and evaluation
                    beta = min(evaluation, beta)
                    # if alpha is bigger than beta, then break out of the recursion and effectively prune this branch
                    if alpha > beta: break
                # The function returns the lowest value and the best move to take
                return v, bestMove

        # The getAction function runs the alphaBeta function and returns the best action to take
        return alphaBeta(gameState, 0, 0)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
