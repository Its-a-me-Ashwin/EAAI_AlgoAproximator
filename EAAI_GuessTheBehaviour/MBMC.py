from vis_gym import *

env = game # Game already initialized withing vis_gym.py

obs, reward, done, info = env.reset() # Reset the environment

#env.render() # Uncomment to game state info

refresh(obs, reward, done, info)  # First call to initialize the game screen

while not done: # Loop until game is completed
	input()
	action = env.action_space.sample()				# Random action
	obs, reward, done, info = env.step(action)      # Take a step in the environment
	refresh(obs, reward, done, info)
input()