# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discountRate (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state
  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)
    self.qValues = util.Counter()


  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    """Description:
    [If the state has not been seen, then return 0
     otherwise, return the respective qvalue]
         """
    """ YOUR CODE HERE """
    if (state,action) in self.qValues:
      qvalue = self.qValues[(state,action)]
    else:
      qvalue = 0
    return qvalue

    return 0

  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    """Description:
    [Here we call our max function, and generate the largest value
    of an action. If none exist, we will return 0, as the state is 
    unexplored]

        """
    """ YOUR CODE HERE """
    # util.raiseNotDefined()

    max = self.generateMax(state)
    if not max:
      return 0

    return max
    """ END CODE """


  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    """Description:
    [We generate the max move, from our max generate function. ]
    """
    """ YOUR CODE HERE """

    return self.generateMax(state,useKey=True)

    # util.raiseNotDefined()
    """ END CODE """

  #This is our max generation function, it will 
  #return the largest value or action depending 
  #on the call
  def generateMax(self,state,useKey=False):
    legalActions = self.getLegalActions(state)
    if not legalActions: return None

    actionList = util.Counter()
    bestValue = float('-inf')
    for action in legalActions:
      value = self.getQValue(state,action)
      # if value <0: continue
      actionList[action] = value
      if value > bestValue:
        bestValue = value
    if useKey:
      return actionList.argMax()
    else:
      return bestValue

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None

    """Description:
    [We use the epsilon to start applying our learning, when 
     the coin flip is less than epsilon, we will pick
     a random action to learn. otherwise, we will pick 
     a learned action]
         """
    """ YOUR CODE HERE """

    # return random.choice(legalActions)
    if not legalActions: return None

    coinProb = util.flipCoin(self.epsilon)
    if coinProb: return random.choice(legalActions)
    return self.getPolicy(state)



    return action

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
    """
    """Description:
    [This is pretty much the function given:
    sample = Reward + discount * maxQ(nextState)]
    Q(s,a) = (1-alpha)*Q(s,a) + alpha*sample
        """
    """ YOUR CODE HERE """
    sample=reward

    if self.getLegalActions(nextState):
      sample = reward + self.discountRate * self.generateMax(nextState)
    self.qValues[(state,action)] = (1-self.alpha)*self.getQValue(state,action) + self.alpha*sample
    """ END CODE """

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    self.weights = util.Counter()

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    """Description:
   [Here we follow the formula:
     Q(s,a) = SUM ( Wi * feature(s,a)) for all features]
         """
    """ YOUR CODE HERE """
    q = 0
    currentFeatures = self.featExtractor.getFeatures(state,action)
    for feature in currentFeatures:
      score = currentFeatures[feature]
      q += self.weights[feature] * score
    return q
    # util.raiseNotDefined()
    """ END CODE """

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    """Description:
    [Again this follows the formula which is:
     correction = reward + discount*value(nextState) -Q(s)
     wi = w * alpha*correction * feature] for all weights
         """
    """ YOUR CODE HERE """
    correction = reward + self.discountRate*self.getValue(nextState) - self.getQValue(state, action)
    features = self.featExtractor.getFeatures(state, action)
    for feature in features:
        self.weights[feature] += self.alpha * correction * features[feature]

    """ END CODE """

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      print ''
      # util.raiseNotDefined()
