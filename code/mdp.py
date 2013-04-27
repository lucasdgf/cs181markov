

# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

# make pi global so computation need only occur once
PI = {}
EPSILON = .001


# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  #for ele in PI:
    #print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):

  return PI[score]

# define transition matrix/ function
def T(a, s, s_prime):
  # takes an action a, current state s, and next state s_prime
  # returns the probability of transitioning to s_prime when taking action a in state s
  
  probability = 0.0

  # -2 -1 0 1 2
  for w in range(-2, 3):
    # hit the wedge (0)
    if abs(w) == 0:
      p_wedge = 0.4
    # hit region outside the wedge (-1 or 1)
    elif abs(w) == 1:
      p_wedge = 0.2
    # hit region outside of that (-2 or 2)
    else:
      p_wedge = 0.1

    # get the wedge and do % to loop around in case of going around circle
    wedge = (a.wedge + w) % throw.NUM_WEDGES

    # same thing, but now for the ring
    for r in range(-2, 3):
      # hit the ring
      if abs(r) == 0:
        p_ring = 0.4
      # hit region outside the ring
      elif abs(r) == 1:
        p_ring = 0.2
      # hit region outside of that
      else:
        p_ring = 0.1

      # get the ring and do % to loop around in case of going around circle
      ring = abs(a.ring + r)

      score = throw.location_to_score(throw.location(ring, wedge))
      if score == s - s_prime:
        probability += p_wedge * p_ring

  return probability


def infiniteValueIteration(gamma):
  # takes a discount factor gamma and convergence cutoff epsilon
  # returns

  V = {}
  Q = {}
  V_prime = {}
  
  states = darts.get_states()
  actions = darts.get_actions()

  notConverged = True

  # intialize value of each state to 0
  for s in states:
    V[s] = 0
    Q[s] = {}

  # until convergence is reached
  while notConverged:

    # store values from previous iteration
    for s in states:
      V_prime[s] = V[s]

    # update Q, pi, and V
    for s in states:
      for a in actions:

        # given current state and action, sum product of T and V over all states
        summand = 0
        for s_prime in states:
          summand += T(a, s, s_prime)*V_prime[s_prime]

        # update Q
        Q[s][a] = darts.R(s, a) + gamma*summand

      # given current state, store the action that maximizes V in pi and the corresponding value in V
      PI[s] = actions[0]
      V[s] = Q[s][PI[s]]                                                        
      for a in actions:
        if V[s] <= Q[s][a]:
          V[s] = Q[s][a]
          PI[s] = a

    notConverged = False
    for s in states:
      if abs(V[s] - V_prime[s]) > EPSILON:
        notConverged = True
  
