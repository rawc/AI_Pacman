# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util, time

from game import Agent
from game import Actions

from captureAgents import CaptureAgent
import distanceCalculator
import game
from util import nearestPoint

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  return [eval(first)(firstIndex), eval(second)(secondIndex)]
class ReflexAgent(CaptureAgent):
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
    some Directions.X for some X in the set {North, South, West, East, Stop}
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
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPosition = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    foodList = oldFood.asList()

    # To find the closest food and closest ghost, I sort the respective lists by distance from the ghost

    foodList.sort(lambda x,y: util.manhattanDistance(newPosition, x)-util.manhattanDistance(newPosition, y))
    closestFoodScore=float(util.manhattanDistance(newPosition, foodList[0]))

    ghostPositions=[(int(Ghost.getPosition()[0]),int(Ghost.getPosition()[1])) for Ghost in newGhostStates]
    ghostPositions.sort(lambda x,y: util.manhattanDistance(newPosition, x)-util.manhattanDistance(newPosition, y))
    closestGhostScore=float(util.manhattanDistance(newPosition, ghostPositions[0]))

    # if we are currently at a Ghost or Food return the respective score
    if closestGhostScore == 0:
      return -200

    if closestFoodScore == 0:
      return 1


    #guide the closest food, with subtracting the closest ghost at a higher cost
    score =  (1.0/closestFoodScore) - (2 * 1.0/closestGhostScore)
    return score
 

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
    self.evaluationFunction = util.lookup('evaluationFunction', globals())
    self.treeDepth = int(depth)

class OffensiveReflexAgent(ReflexAgent):
  """
    Your minimax agent (question 2)
  """

  index = 0 # Pacman is always agent index 0
  # evaluationFunction = eval(betterEvaluationFunction)

  #util.lookup('betterEvaluationFunction', globals())
  treeDepth = int(2)

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    retVal = self.miniMax(gameState,0,0)
    return retVal[1]


  # We will use this as our base function for the recursive call
  # We will maximize the Pacmans state and minmize the ghost
  def miniMax(self, gameState, currentIndex, currentDepth, alpha=None, beta=None):
    if currentIndex >= gameState.getNumAgents():
      currentIndex = 0
      currentDepth += 1

    if currentDepth == self.treeDepth:
        return (self.evaluationFunction(gameState), 'none')

    if currentIndex == 0:
        return self.maxValue(gameState, currentIndex, currentDepth)
    else:
        return self.minValue(gameState, currentIndex, currentDepth)

  def minValue(self,gameState,index, currentDepth, alpha=None, beta = None):
    moves = gameState.getLegalActions(index)
    bestScore = float('inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState), 'none')

    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score, newMove = self.miniMax(nextState,index+1,currentDepth)
      if score < bestScore:
        bestMove = move
        bestScore = score

    return (bestScore,bestMove)

  def maxValue(self,gameState,index, currentDepth, alpha=None, beta=None):
    moves = gameState.getLegalActions(index)
    bestScore = float('-inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState), 'none')

    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score, newMove = self.miniMax(nextState,index+1,currentDepth)
      if score > bestScore:
        bestMove = move
        bestScore = score

    return (bestScore,bestMove)
  def betterEvaluationFunction(currentGameState):


    numOfFood = currentGameState.getNumFood()
    currentPositon = currentGameState.getPacmanPosition()

    newGhostStates = currentGameState.getGhostStates()
    ghostPositions=[(int(Ghost.getPosition()[0]),int(Ghost.getPosition()[1])) for Ghost in newGhostStates]

    ghostPositions.sort(lambda x,y: util.manhattanDistance(currentPositon, x)-util.manhattanDistance(currentPositon, y))
    closestGhostScore=util.manhattanDistance(currentPositon, ghostPositions[0])
    
    if closestGhostScore == 0:
      return -200

    return currentGameState.getScore() - (5 * numOfFood) - (20 * 1/closestGhostScore)
    
class DefensiveReflexAgent(ReflexAgent):
  """
    Your minimax agent (question 2)
  """
  self.index = 0 # Pacman is always agent index 0
  self.evaluationFunction = util.lookup(evalFn, globals())
  self.treeDepth = int(2)


  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.treeDepth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    retVal = self.miniMax(gameState,0,0)
    return retVal[1]


  # We will use this as our base function for the recursive call
  # We will maximize the Pacmans state and minmize the ghost
  def miniMax(self, gameState, currentIndex, currentDepth, alpha=None, beta=None):
    if currentIndex >= gameState.getNumAgents():
      currentIndex = 0
      currentDepth += 1

    if currentDepth == self.treeDepth:
        return (self.evaluationFunction(gameState), 'none')

    if currentIndex == 0:
        return self.maxValue(gameState, currentIndex, currentDepth)
    else:
        return self.minValue(gameState, currentIndex, currentDepth)

  def minValue(self,gameState,index, currentDepth, alpha=None, beta = None):
    moves = gameState.getLegalActions(index)
    bestScore = float('inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState), 'none')

    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score, newMove = self.miniMax(nextState,index+1,currentDepth)
      if score < bestScore:
        bestMove = move
        bestScore = score

    return (bestScore,bestMove)

  def maxValue(self,gameState,index, currentDepth, alpha=None, beta=None):
    moves = gameState.getLegalActions(index)
    bestScore = float('-inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState), 'none')

    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score, newMove = self.miniMax(nextState,index+1,currentDepth)
      if score > bestScore:
        bestMove = move
        bestScore = score

    return (bestScore,bestMove)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.treeDepth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    retVal = self.miniMax(gameState, 0, 0, float('-inf'), float('inf'))
    return retVal[1]

  #This follows the same logic as before, but now we will prune
  def miniMax(self, gameState, currentIndex, currentDepth, alpha=None, beta=None):
    if currentIndex >= gameState.getNumAgents():
      currentIndex = 0
      currentDepth += 1

    if currentDepth == self.treeDepth:
        return (self.evaluationFunction(gameState), 'none')

    if currentIndex == 0:
        return self.maxValue(gameState, currentIndex, currentDepth, alpha, beta)
    else:
        return self.minValue(gameState, currentIndex, currentDepth, alpha, beta)

  def minValue(self,gameState,index, currentDepth, alpha=None, beta = None):
    moves = gameState.getLegalActions(index)
    bestScore = float('inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState),'none')

    for move in moves:
      if move == Directions.STOP: continue 
      nextState = gameState.generateSuccessor(index,move)
      score,newMove = self.miniMax(nextState,index+1,currentDepth, alpha, beta)
      if score < bestScore:
        bestMove = move
        bestScore = score
      if score <= alpha: 
        return (score, bestMove)
      beta = min(beta, score)
    return (bestScore,bestMove)

  def maxValue(self,gameState,index, currentDepth, alpha=None, beta=None):
    moves = gameState.getLegalActions(index)
    bestScore = float('-inf')
    bestMove = None
    if not moves: return (self.evaluationFunction(gameState),'none')

    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score,newMove = self.miniMax(nextState,index+1,currentDepth,alpha, beta)
      if score > bestScore:
        bestMove = move
        bestScore = score
      if score >= beta:
        return (score, bestMove)
      alpha = max(alpha, score)
    return (bestScore,bestMove)

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.treeDepth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"

    retVal = self.miniMax(gameState, 0, 0)
    return retVal[1]

  # same logic as before, but now we will be using the expectedValue
  # instead of using the minimizer function
  # this will preform much better
  def miniMax(self, gameState, currentIndex, currentDepth):
    #our base function
    # if the index has reached the total number of agents
    # we have finished our cylcle, so we increase the depth

    if currentIndex >= gameState.getNumAgents():
      currentIndex = 0
      currentDepth += 1

    # if we have finished the required depth, process the gamestate
    if currentDepth == self.treeDepth:
        return (self.evaluationFunction(gameState), 'none')

    # if pacman, calculate the max value, for pacman to win
    if currentIndex == 0:
        return self.maxValue(gameState, currentIndex, currentDepth)
    else:
    # if ghost, lets calculate the expected values, of each ghost
        return self.expectedValue(gameState, currentIndex, currentDepth)

  def expectedValue(self,gameState,index, currentDepth):
    moves = gameState.getLegalActions(index)
    if not moves: return (self.evaluationFunction(gameState),'none')
    bestScore = 0
    moveProbability = 1.0/len(moves)
    bestMove = None
    # loop through all the possible moves of the ghosts
    # calculate the score of each move with our probability 
    # now each move has an expected score associated with it
    # so we know where the ghost will probably be
    for move in moves:
      if move == Directions.STOP: continue 
      nextState = gameState.generateSuccessor(index,move)
      score,newMove = self.miniMax(nextState,index+1,currentDepth)
      bestScore += score * moveProbability
      bestMove = newMove

    return (bestScore,bestMove)


  def maxValue(self,gameState,index, currentDepth):
    moves = gameState.getLegalActions(index)
    if not moves: return (self.evaluationFunction(gameState),'none')

    bestScore = float('-inf')

    bestMove = None
    for move in moves:
      if move == Directions.STOP: 
        continue 
      nextState = gameState.generateSuccessor(index,move)
      score,newMove = self.miniMax(nextState,index+1,currentDepth)
      if score > bestScore:
        bestMove = move
        bestScore = score
    
    return (bestScore,bestMove)

      
def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This function takes the number of food and subtracts frome the current score
                 in order to guide the pacman into getting the the very last food. (The score increases 
                 as he eats more). If we encouter a ghost in our our nextState, we will return -200, to
                 stay as far away as possible. Otherwise, we will subtract the reciprical of the closest
                 ghost, so that as the ghost gets farther the score goes up. Of course there is a higher
                 weight attached to the ghosts, as we do not want the pacman to die.
  """
  "*** YOUR CODE HERE ***"


  numOfFood = currentGameState.getNumFood()
  currentPositon = currentGameState.getPacmanPosition()

  newGhostStates = currentGameState.getGhostStates()
  ghostPositions=[(int(Ghost.getPosition()[0]),int(Ghost.getPosition()[1])) for Ghost in newGhostStates]

  ghostPositions.sort(lambda x,y: util.manhattanDistance(currentPositon, x)-util.manhattanDistance(currentPositon, y))
  closestGhostScore=util.manhattanDistance(currentPositon, ghostPositions[0])
  
  if closestGhostScore == 0:
    return -200

  return currentGameState.getScore() - (5 * numOfFood) - (20 * 1/closestGhostScore)
  
# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

