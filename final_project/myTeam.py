
from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util
from game import Directions
from game import Actions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'alphaAgent', second = 'betaAgent'):
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

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on). 
    
    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)
    IMPORTANT: This method may run for at most 15 seconds.
    """

    ''' 
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py. 
    '''
    CaptureAgent.registerInitialState(self, gameState)

    ''' 
    Your initialization code goes here, if you need any.
    '''
    if self.red:
      CaptureAgent.registerTeam(self, gameState.getRedTeamIndices())
    else:
      CaptureAgent.registerTeam(self, gameState.getBlueTeamIndices())

    self.initBoundry(gameState)
    self.initNumberOfFood(gameState)

  """UTILITY FUNCTIONS"""

  #SEARCH
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

  #ASTAR
  def foodHeuristic(foodList):
    farthestFood = 0
    for food in foodList:
      farthestFoodDistance =(util.manhattanDistance(position,food))
      if farthestFoodDistance > farthestFood:
        farthestFood = farthestFoodDistance
    return farthestFood

  def aStarSearch(problem):
    return search(util.PriorityQueue(), problem, astar, eval(foodHeuristic))

  def chooseAction(self, gameState):
    """
    Picks among the actions with the highest Q(s,a).
    """
    myScaredTimer = gameState.getAgentState(self.index).scaredTimer
    actions = gameState.getLegalActions(self.index)
    
    # You can profile your evaluation time by uncommenting these lines
    start = time.time()
    values = [self.evaluate(gameState, a) for a in actions]
    # print 'eval time for agent %d: %.4f' % (self.index, time.time() - start)

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
    successor = self.getSuccessor(gameState, action)
    currentAgent = successor.getAgentState(self.index)
    myPos = successor.getAgentState(self.index).getPosition()

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    numOfInvaders = len(invaders)


    closestEnemie = 100000000
    closestEnemieObject = None
    enemiesNearBy = False

    opponents = self.getOpponents(gameState)
    for enemy in range(0,len(opponents)):
      enemyIndex = opponents[enemy]
      enemyObject = gameState.getAgentState(enemyIndex)
      enemyPos = enemyObject.getPosition()

      if enemyPos:
        enemiesNearBy = True
        distanceBetweenMates = self.getMazeDistance(myPos, enemyPos)
        if distanceBetweenMates < closestEnemie:
          closestEnemie = distanceBetweenMates
          closestEnemieObject = enemyObject

    minFoodDistance = 10000
    minFood = (0,0)
    foodList = self.getFood(gameState).asList()
    for x,y in foodList:
      distance = self.getMazeDistance(myPos,(x,y))

      if distance < minFoodDistance:
        minFoodDistance = distance
        minFood = (x,y)

    foodDefendingList = self.getFoodYouAreDefending(gameState).asList()
    foodDefending = self.getFoodYouAreDefending(gameState)
    foodLeft = 0 
    for x,y in foodDefendingList:
      foodLeft += 1

    foodEaten = self.numberOfFood - foodLeft
    foodEatenPercentage = float(foodEaten) / float(self.numberOfFood)

    features = weights = 0

    """CASES WHERE PACMAN MUST OBEY STARTEGY IMMEDIATLEY"""


    if closestEnemie <= 2 and not closestEnemieObject.isPacman and currentAgent.isPacman:
      features = self.startFeatures(gameState, action)
      weights = self.startWeights(gameState, action) 
      # print 'DEFENSE - CLOSE ATTACKER: LEAVING OFFENSE' 
      return features * weights

    if closestEnemie <= 1 and not closestEnemieObject.isPacman and not currentAgent.isPacman:
      features = self.defensiveFeatures(gameState, action)
      weights = self.defensiveWeights(gameState, action) 
      self.refreshStartGoal(gameState, closestEnemieObject.getPosition())
      # features = self.startFeatures(gameState, action)
      # weights = self.startWeights(gameState, action)
      # print 'DEFENSE - CLOSE DEFENDER: STAYING DEFENSE' 

      return features *weights

    if currentAgent.isPacman:
        features = self.offensiveFeatures(gameState, action)
        weights = self.offensiveWeights(gameState, action)
        # print 'OFFFENSE - PACMAN'
        return features * weights      

    """DEFENSE"""
    if numOfInvaders > 0:
      features = self.defensiveFeatures(gameState, action)
      weights = self.defensiveWeights(gameState, action)
      # print 'DEFENSE - INAVDER' 
      

    else:
      #START
      if minFoodDistance > 7:
        self.refreshStartGoal(gameState)
        features = self.startFeatures(gameState, action)
        weights = self.startWeights(gameState, action)
        # print 'START - EXPLORING' 

      else:
        #OFFENSE
        features = self.offensiveFeatures(gameState, action)
        weights = self.offensiveWeights(gameState, action)
        # print 'OFFENSE' 


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

  def offensiveFeatures(self,gameState,action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    features['successorScore'] = self.getScore(successor)

    # Compute distance to the nearest food
    foodList = self.getFood(successor).asList()
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      myPos = successor.getAgentState(self.index).getPosition()
      minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
      features['distanceToFood'] = minDistance

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition()]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      features['ghostDistance'] = min(dists)
    myPos = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
    features['distanceToBoundry'] = self.distanceFromBoundryLine(gameState,myPos)

    closestCapsule , closestCapsuleDistamce = self.getClosestCapsule(gameState, action)
    features['distanceToPellet'] = closestCapsuleDistamce + 1

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def getClosestCapsule (self, gameState, action):
    myPos = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
    closestCapsule = (0,0)
    closestCapsuleDistamce = 10000
    for capsule in self.getCapsules(gameState):
      capsuleDist = self.getMazeDistance(myPos, capsule)
      if capsuleDist < closestCapsuleDistamce:
        closestCapsuleDistamce = capsuleDist
        closestCapsule = capsule
    return closestCapsule, closestCapsuleDistamce
  def offensiveWeights (self,gameState,action):
    myPos = self.getSuccessor(gameState, action).getAgentState(self.index).getPosition()
    successor = self.getSuccessor(gameState, action)
    currentAgent = successor.getAgentState(self.index)
    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]

    ghostDistance = 10
    for enemie in enemies:
      if enemie.scaredTimer > 0:
        ghostDistance = -1

    return {'successorScore': 100, 'distanceToFood': -2, 'ghostDistance': ghostDistance, 
    'distanceToBoundry':-1, 'distanceToPellet':-1,'stop': -100, 'reverse': -1}


  def checkIfEnemyIsAttacking(self,gameState,action):
    successor = self.getSuccessor(gameState, action)

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    foodDefendingList = self.getFoodYouAreDefending(gameState).asList()
    opponents = self.getOpponents(gameState)
    
    for enemy in range(0,len(opponents)):
      enemyIndex = opponents[enemy]
      enemyObject = gameState.getAgentState(enemyIndex)
      enemyPos = enemyObject.getPosition()
      if enemyPos in foodDefendingList:
        return True
    return False

  def teamDistance(self,gameState, action):
    teamPositions = []
    for teamMate in self.getTeam(gameState):
      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(teamMate)
      myPos = myState.getPosition()
      teamPositions.append((teamMate,myPos))
    distanceBetweenMates = self.getMazeDistance((teamPositions[0])[1], (teamPositions[1])[1])
    return distanceBetweenMates


  def percentageOfFoodDefendingEaten(self, gameState):
    foodDefendingList = self.getFoodYouAreDefending(gameState).asList()
    foodDefending = self.getFoodYouAreDefending(gameState)
    foodLeft = 0 
    for x,y in foodDefendingList:
      foodLeft += 1

    foodEaten = self.numberOfFood - foodLeft
    foodEatenPercentage = float(foodEaten) / float(self.numberOfFood)
    return foodEatenPercentage
    
  def defensiveFeatures(self, gameState, action):
    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    # Computes whether we're on defense (1) or offense (0)
    features['onDefense'] = 1
    if myState.isPacman: features['onDefense'] = 0

    features['teamDistance']=self.teamDistance(gameState,action)

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
      distance =     distancer.getDistance((0,0),(x,y))

      if distance > maxDistance:
        maxDistance = distance
        maxFood = (x,y)

    features['farthestRedFood'] = 1/maxDistance
    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    return features

  def defensiveWeights(self, gameState, action):
    distanceWeight = 0
    successor = self.getSuccessor(gameState, action)
    myPos = successor.getAgentState(self.index).getPosition()

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    invaders = [a for a in enemies if a.isPacman and a.getPosition() != None]
    dists = [self.getMazeDistance(myPos, a.getPosition()) for a in invaders]

    invaderDistanceValue = -50
    scaredTimer = gameState.getAgentState(self.index).scaredTimer


    if self.percentageOfFoodDefendingEaten(gameState) > 0.45:
      invaderDistanceValue = - 10000

    if scaredTimer > 0:
      invaderDistanceValue= 10


    return {'numInvaders': -1000, 'onDefense': 100, 'invaderDistance': invaderDistanceValue, 'stop': -100, 'reverse': -2}

  def startFeatures(self, gameState, action):

    features = util.Counter()
    successor = self.getSuccessor(gameState, action)

    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()
    features['center'] = self.distanceFromStartCorner(gameState,myPos)
    features['isCenter'] = 1

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1
    return features

  def startWeights(self, gameState, action):
    return{
      'center' : -50,
      'isCenter': 100,
      'stop': -100, 
      'reverse': -2
    }

  def goBackHomeFeatures(self, gameState, action):

    features = util.Counter()
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    features['foodToDefendDist'] = self.getClosestFoodToDefend(gameState,action)
    features['isCenter'] = 1

    if action == Directions.STOP: features['stop'] = 1
    rev = Directions.REVERSE[gameState.getAgentState(self.index).configuration.direction]
    if action == rev: features['reverse'] = 1

    enemies = [successor.getAgentState(i) for i in self.getOpponents(successor)]
    ghosts = [a for a in enemies if not a.isPacman and a.getPosition()]
    features['numGhosts'] = len(ghosts)
    if len(ghosts) > 0:
      dists = [self.getMazeDistance(myPos, a.getPosition()) for a in ghosts]
      features['ghostDistance'] = min(dists)
    return features

  def goBackHomeWeights(self, gameState, action):
    return{
      'foodToDefendDist' : -500,
      'isCenter': 100,
      'stop': -100, 
      'reverse': -2,
      'ghostDistance' :10

    }
  def distanceFromBoundryLine(self,gameState,position):
    x,y = position
    distanceFromMax = self.maxY - y 
    distanceFromMin = y - self.minY

    if distanceFromMax < distanceFromMin:
      if distanceFromMax == 0: return 0
      else: return 1.0/distanceFromMax
    else:
      if distanceFromMin == 0: return 0
      else: return 1.0/distanceFromMin

  def distanceFromStartCorner(self,gameState,position):
    return self.getMazeDistance(position,(self.centerX, self.centerY))

  def initNumberOfFood(self, gameState):
    foodDefendingList = self.getFoodYouAreDefending(gameState).asList()
    foodDefending = self.getFoodYouAreDefending(gameState)
    self.numberOfFood = 0
    for x,y in foodDefendingList:
      if foodDefending[x][y]: self.numberOfFood += 1

  def getClosestFoodToDefend(self, gameState, action):
    successor = self.getSuccessor(gameState, action)
    myState = successor.getAgentState(self.index)
    myPos = myState.getPosition()

    foodDefendingList = self.getFoodYouAreDefending(gameState).asList()
    closestFoodDist = 1000
    closestFood = (0,0)
    for food in foodDefendingList:
      foodDist = self.getMazeDistance(myPos,food)
      if foodDist < closestFoodDist:
        closestFoodDist = foodDist

    return foodDist


  def refreshStartGoal(self,gameState, enemyPos = None):
    foodToEat = self.getFood(gameState).asList()
    allowedFoods = []
    for foodX, foodY in foodToEat:
      if self.minY <= foodY <= self.maxY :
        allowedFoods.append((foodX,foodY))

    # if not allowedFoods: return
    # if not enemyPos:
    #   minFoodToMe = min(allowedFoods)
    #   # print('closest food to my area is {}'.format(minFoodToMe))
    #   self.centerX = minFoodToMe[0]
    #   self.centerY = minFoodToMe[1]
    # else:
    #   minFoodToMe = min(allowedFoods)
    #   allowedFoods.remove(minFoodToMe)
    #   minFoodToMe = min(allowedFoods)

    #   # print('closest food to my area is {}'.format(minFoodToMe))
    #   self.centerX = minFoodToMe[0]
    #   self.centerY = minFoodToMe[1]

class alphaAgent(ReflexCaptureAgent):

  def initBoundry(self, gameState):
    self.minY = int(gameState.getWalls().height / 2)
    self.maxY = gameState.getWalls().height
    self.centerX = int(gameState.getWalls().width / 2)
    self.centerY = int((self.maxY + self.minY) / 2) - 1

    foodToEat = self.getFood(gameState).asList()
    # print (min(foodToEat))
    # self.centerX = min(foodToEat)[0]

    allowedFoods = []
    for foodX, foodY in foodToEat:
      if self.minY <= foodY <= self.maxY :
        allowedFoods.append((foodX,foodY))
    if not allowedFoods: return


    minFoodToMe = min(allowedFoods)
    self.centerX = minFoodToMe[0]
    self.centerY = minFoodToMe[1]


  def moveInAgentBoundry(self,gameState, position):
    x,y = position
    if self.minY <= y <= self.maxY:
      return True
    return False

class betaAgent(ReflexCaptureAgent):

  def initBoundry(self, gameState):
    self.maxY = int(gameState.getWalls().height / 2)
    self.minY = 0
    self.centerX = int(gameState.getWalls().width / 2)
    self.centerY = int((self.maxY + self.minY) / 2) - 1

    foodToEat = self.getFood(gameState).asList()

    allowedFoods = []
    for foodX, foodY in foodToEat:
      if self.minY <= foodY <= self.maxY :
        allowedFoods.append((foodX,foodY))

    minFoodToMe = min(allowedFoods)
    self.centerX = minFoodToMe[0]
    self.centerY = minFoodToMe[1]



  def moveInAgentBoundry(self,gameState, position):
    x,y =position
    if self.minY <= y <= self.maxY:
      return True
    return False


