# analysis.py
# -----------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

######################
# ANALYSIS QUESTIONS #
######################

# Change these default values to obtain the specified policies through
# value iteration.

def question2():
  answerDiscount = 0.9
  answerNoise = 0.0
  """Description:
  [If we remove noise, the agent will find the right path.]
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise

def question3a():
  answerDiscount = 0.2
  answerNoise = 0
  answerLivingReward = 0.0
  """Description:
  If we remove the living reward, the agent will not have an
  incentive to hang around the board, making it want to go to
  the closest path. Also, lowering the discount, will give the
  agent less reward for staying longer, allowing the agent to risk
  the cliff instead of the longer path
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3b():
  answerDiscount = 0.1
  answerNoise = 0.1
  answerLivingReward = 0.8
  """Description:
  With more noise, the agent will more fearful of the dangerous areas
  and will avoid the cliff more. Also, with an increased living reward,
  the agent will hang around the board longer, as its happy living.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3c():
  answerDiscount = 0.5
  answerNoise = 0.1
  answerLivingReward = 0.0
  """Description:
  Same as A , but now with a higher discount, the agent
  will travel to the farther goal, and avoid the cliff.
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3d():
  answerDiscount = 0.6
  answerNoise = 0.5
  answerLivingReward = 0.0
  """Description:
  [With a higher discount the agent will want to explore more
  leading it to the further exit. In addition, the higher noise
  will keep it from the cliffs.]
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question3e():
  answerDiscount = 0.9
  answerNoise = 0.2
  answerLivingReward = 1
  """Description:
  [If the living reward is 1 then the agent will have no wish to find any
  exit. It is happy running around.]
  """
  """ YOUR CODE HERE """

  """ END CODE """
  return answerDiscount, answerNoise, answerLivingReward
  # If not possible, return 'NOT POSSIBLE'

def question6():
  answerEpsilon = 0.5
  answerLearningRate = None
  """Description:
  [There is no way to generate a better policy than the q-learners.
  ]
  """
  """ YOUR CODE HERE """
  return 'NOT POSSIBLE'
  """ END CODE """
  return answerEpsilon, answerLearningRate
  # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
  print 'Answers to analysis questions:'
  import analysis
  for q in [q for q in dir(analysis) if q.startswith('question')]:
    response = getattr(analysis, q)()
    print '  Question %s:\t%s' % (q, str(response))
