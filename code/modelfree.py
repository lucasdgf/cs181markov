import random
import darts
import throw

# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.

states = []
actions = []
Q = {}

alpha = 0
gamma = 0

"""def start_game():
  return (throw.location(throw.INNER_RING, throw.NUM_WEDGES)) 

def get_target(score):
  if score <= throw.NUM_WEDGES: 
    return throw.location(throw.SECOND_PATCH, score)  
  return (throw.location(throw.INNER_RING, throw.NUM_WEDGES))"""

# Exploration/exploitation strategy one
def ex_strategy_one():
  return random.choice([0, 1])

# Exploration/exploitation strategy two
def ex_strategy_two(num_iterations):
  return random.random() < 1. / (2 + num_iterations)

# Q-learning!
def start_game():
    global states, actions

    states = darts.get_states()
    actions = darts.get_actions()

    Q = [[0 for a in actions] for s in states]

def get_target(score):
    to_explore = ex_strategy_one()
    # to_explore = ex_strategy_two(score)

    if to_explore:
        return random.choice(actions)
    else:
        return max(Q[score], key = Q[scores].get)

def q_learning(s, s_prime, a, r):
    Q[s][a] += alpha * (r + gamma * (MAXSOMETHINGDEARLORD) - Q[s][a])