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

alpha = 0.5
gamma = 0.5

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
    global states, actions, Q
    states = darts.get_states()
    actions = darts.get_actions()

    for s in states:
        Q[s] = {}
        for a in range(len(actions)):
            Q[s][a] = 0

    return throw.location(throw.INNER_RING, throw.NUM_WEDGES)

def get_target(score):
    #to_explore = ex_strategy_one()
    to_explore = ex_strategy_two(score)

    if to_explore:
        return random.choice(actions)
    else:
        action = max_dict(Q, score)
        return actions[action] if action else random.choice(actions)

def q_learning(s, s_prime, a):
    global Q

    r = darts.R(s_prime, a)
    Q[s][a] += alpha * (r + gamma * max_dict(Q, s_prime) - Q[s][a])

def max_dict(d, s):
    max_k = 0
    max_v = 0
    for k, v in d[s].iteritems():
        if v >= max_v:
            max_v = v
            max_k = k
    return max_k