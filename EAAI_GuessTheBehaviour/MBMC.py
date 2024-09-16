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

while not done: # Loop until game is completed
	input()
	action = env.action_space.sample()				# Random action
	obs, reward, done, info = env.step(action)
	if gui_flag:
		refresh(obs, reward, done, info)
	print(obs, reward, done, info)
input()