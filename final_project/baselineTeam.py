# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

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

##########
# Agents #
##########

class ReflexCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    myScaredTimer = gameState.getAgentState(self.index).scaredTimer
    actions = gameState.getLegalActions(self.index)
    
    # You can profile your evaluation time by uncommenting these lines
    start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

    maxValue = max(values)
    bestActions = [a for a, v in zip(actions, values) if v == maxValue]

    return random.choice(bestActions)

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def evaluate(self, gameState, action):
    """
    Computes a linear combination of features and feature weights
    """
    features = self.getFeatures(gameState, action)
    weights = self.getWeights(gameState, action)
    return features * weights

  def getFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)
    return features

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'successorScore': 1.0}

class OffensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that seeks food. This is an agent
  we give you to get an idea of what an offensive agent might look like,
  but it is by no means the best or only way to build an offensive agent.
  """
  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance
    return features

  def getWeights(self, gameState, action):
    return {'successorScore': 100, 'distanceToFood': -1}

class DefensiveReflexAgent(ReflexCaptureAgent):
  """
  A reflex agent that keeps its side Pacman-free. Again,
  this is to give you an idea of what a defensive agent
  could be like.  It is not the best or only way to make
  such an agent.
  """

  def teamDistance(self,gameState, action):
    teamPositions = []
    for teamMate in self.getTeam(gameState):
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(teamMate)
      myPos = myState.getPosition()
      teamPositions.append((teamMate,myPos))
    # print('team postions are {}'.format(teamPositions))
    distanceBetweenMates = self.getMazeDistance((teamPositions[0])[1], (teamPositions[1])[1])
    # print distanceBetweenMates
    return distanceBetweenMates


  def getFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    # print ('pacman is on defense ? {}'.format(features['onDefense']))
    # print(myState)
    # print(self.red)
    # print('team is {}'.format((self.getTeam(gameState))))
    # print('index is {}'.format(self.index))
    # print('my pos is {}'.format(myPos))
    features['teamDistance']=self.teamDistance(gameState,action)

    print'/////////////'
    # print(distanceCalculator.)
    # Computes distance to invaders we can see
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    features['numInvaders'] = len(invaders)
    if len(invaders) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
      features['invaderDistance'] = min(dists)

    redFood = self.getFoodYouAreDefending(gameState).asList()
    maxDistance = 0
    maxFood = (0,0)
    
    distancer = distanceCalculator.Distancer(gameState.data.layout)
    for x,y in redFood:
      # print 'red food are {} {} '.format(x,y)
      distance =     distancer.getDistance(myPos,(x,y))
      # print 'distance from redFood is {}'.format(distance)

      if distance > maxDistance:
        maxDistance = distance
        maxFood = (x,y)

    # print('max food is {}'.format(maxFood))
    features['farthestRedFood'] = maxDistance
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getWeights(self, gameState, action):
    distanceWeight = 0
    successor = self.getSuccessor(gameState, action)
    myPos = successor.getAgentState(self.index).getPosition()

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]
    # if dists:
      # print ('closest invader is {}'.format(min(dists)))
      # if min(dists) < 10 :
        # distanceWeight = -5
    invaderDistanceValue = -1000
    # scaredTimer = gameState.getAgentState(self.index).scaredTimer
    # if scaredTimer > 0:
    #   invaderDistanceValue= 1000

      # print('timer {}'.format(m.scaredTimer))

    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': invaderDistanceValue, 'stop': -100, 'reverse': -2, 'teamDistance':distanceWeight, 'farthestRedFood':0}
