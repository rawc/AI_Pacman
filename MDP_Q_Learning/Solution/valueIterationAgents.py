# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discountRate = 0.9, iters = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    self.mdp = mdp
    self.discountRate = discountRate
    self.iters = iters
    self.values = util.Counter() # A Counter is a dict with default 0

    """Description:
    [This is the base equation. We loop through all the itertions of learning
    and then we loop through all the possible values and ad return the best value.
    (arg max a). Then we update the state values with the counters.]
    """
    """ YOUR CODE HERE """

    for i in range(iters):
      counter = util.Counter()
      for state in mdp.getStates():
        bestValue = None
        for action in mdp.getPossibleActions(state):
          value = self.getQValue(state, action)

          if value > bestValue:
            bestValue = value

          counter[state] = bestValue
      for state in mdp.getStates():
        self.values[state] = counter[state]

    """ END CODE """

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """
    return self.values[state]


    """Description:
    [We return the specific value associated in the value list. This 
    value has been updated many times.]
    """
    """ YOUR CODE HERE """
    # util.raiseNotDefined()
    """ END CODE """


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    """Description:
    Q* (s,a) = SUM (Transition(state,action,nextState)[Reward(state,action,nextState) + GAMMA(MAX_a Q*(next_state))
    """
    """ YOUR CODE HERE """
    qValue = 0
    for nextState, transitionProbability in self.mdp.getTransitionStatesAndProbs(state,action):
      #Sum part of formula
      nextStateReward = self.mdp.getReward(state,action, nextState)  #reward
      qValue += transitionProbability*(nextStateReward + self.discountRate * self.values[nextState]) #SUM(T()*R() + DISCOUNT*values(next_state)
    return qValue
    """ END CODE """

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """

    """Description:
    [ PI(S) = arg max Q* (s,a)
      here we loop through the all the actions
      and calculate the best action based on the 
      sum of all the q values]
    """
    """ YOUR CODE HERE """

    bestAction = None
    bestActionCost = float('-inf')
    nextStatesActions = self.mdp.getPossibleActions(state)
    if not nextStatesActions: return None

    for action in nextStatesActions:
      actionValue = (self.getQValue(state,action))
      if actionValue > bestActionCost:
        bestActionCost = actionValue
        bestAction = action

    return bestAction

    """ END CODE """

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
