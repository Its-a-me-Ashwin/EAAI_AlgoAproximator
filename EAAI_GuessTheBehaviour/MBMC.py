import numpy as np
from vis_gym import *

gui_flag = False # Set to True to enable the game state visualization
setup(GUI=gui_flag)
env = game # Gym environment already initialized within vis_gym.py

obs, reward, done, info = env.reset() # Reset the environment to initial configuration

#env.render() # Uncomment to print game state info

def hash(obs):
	x,y = obs['player_position']
	h = obs['player_health']
	g = obs['guard_in_cell']
	if not g:
		g = 0
	else:
		g = int(g[-1])

	return x*(5*3*5) + y*(3*5) + h*5 + g

if gui_flag:
	refresh(obs, reward, done, info)  # Update the game screen [GUI only]


'''

Complete the function below to do the following:

	1. Run 1000 episodes of the game. An episode refers to starting in some initial configuration and taking actions until a terminal state is reached.
	2. Keep track of gameplay history in an appropriate format for each of the 1000 episodes.
	3. From gameplay history, estimate the probability of victory against each of the guards when taking the fight action.
		a. Keep in mind that given some observation [(X,Y), health, guard_in_cell], a fight action is only meaningful if the last entry corresponding to guard_in_cell is nonzero.
		b. Upon taking the fight action, if the player defeats the guard, the player is moved to a random neighboring cell with UNCHANGED health. (2 = Full, 1 = Injured, 0 = Critical).
		c. If the player loses the fight, the player is still moved to a random neighboring cell, but the health decreases by 1.
		d. Your player might encounter the same guard in different cells in different episodes.

	Finally, return the np array, P which contains four float values, each representing the probability of defeating guards 1-4 respectively.

'''

def estimate_victory_probability():
	"""
    Probability estimator

    Parameters:
    - None

    Returns:
    - P (numpy array): Empirically estimated probability of defeating guards 1-4.
    """
	P = np.zeros(len(env.guards))

	'''

	YOUR CODE HERE


	'''

	return P

