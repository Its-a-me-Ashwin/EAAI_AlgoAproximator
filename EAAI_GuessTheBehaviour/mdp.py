import random

class CastleEscapeMDP:
    def __init__(self):
        # Define a 5x5 grid (numbered from (0,0) to (4,4))
        self.grid_size = 5
        self.rooms = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size)]
        self.goal_room = (4, 4)  # Define the goal room
        
        # Define health states
        self.health_states = ['Full', 'Injured', 'Critical']
        
        # Define the guards with their strengths (affects combat) and keenness (affects hiding)
        self.guards = {
            'G1': {'strength': 0.8, 'keenness': 0.1},  # Guard 1
            'G2': {'strength': 0.6, 'keenness': 0.3},  # Guard 2
            'G3': {'strength': 0.9, 'keenness': 0.2},  # Guard 3
            'G4': {'strength': 0.7, 'keenness': 0.5},  # Guard 4
        }
        
        # Set initial state
        self.current_state = {
            'player_position': (0, 0),
            'player_health': 'Full',
            'guard_positions': {guard: random.choice(self.rooms[:-1]) for guard in self.guards}  # Guards in random rooms (not the goal)
        }

        # Rewards
        self.rewards = {
            'goal': 10000,
            'combat_win': 10,
            'combat_loss': -1000,
            'defeat': -1000
        }
    
    def reset(self):
        """ Resets the game to the initial state """
        self.current_state = {
            'player_position': (0, 0),
            'player_health': 'Full',
            'guard_positions': {guard: random.choice(self.rooms[:-1]) for guard in self.guards}  # Guards in random rooms (not the goal)
        }
    
    def is_terminal(self):
        """ Check if the game has reached a terminal state """
        if self.current_state['player_position'] == self.goal_room:  # Reaching the goal means victory
            return 'goal'
        if self.current_state['player_health'] == 'Critical':  # Losing health 3 times results in defeat
            return 'defeat'
        return False
    
    def move_player(self, action):
        """ Move player based on the action """
        x, y = self.current_state['player_position']
        directions = {
            'UP': (x-1, y),
            'DOWN': (x+1, y),
            'LEFT': (x, y-1),
            'RIGHT': (x, y+1)
        }
        
        # Calculate the intended move
        new_position = directions.get(action, self.current_state['player_position'])
        
        # Ensure new position is within bounds
        if 0 <= new_position[0] < self.grid_size and 0 <= new_position[1] < self.grid_size:
            # 90% chance to move as intended
            if random.random() <= 0.9:
                self.current_state['player_position'] = new_position
            else:
                # 10% chance to move to a random adjacent cell
                adjacent_positions = [directions[act] for act in directions if act != action]
                adjacent_positions = [pos for pos in adjacent_positions if 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size]
                if adjacent_positions:
                    self.current_state['player_position'] = random.choice(adjacent_positions)
        # No movement if out of bounds
        else:
            return "Out of bounds!"
    
    def move_player_to_random_adjacent(self):
        """ Move player to a random adjacent cell without going out of bounds """
        x, y = self.current_state['player_position']
        directions = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        
        # Filter out-of-bounds positions
        adjacent_positions = [pos for pos in directions if 0 <= pos[0] < self.grid_size and 0 <= pos[1] < self.grid_size]
        
        # Move player to a random adjacent position
        if adjacent_positions:
            self.current_state['player_position'] = random.choice(adjacent_positions)
    
    def try_fight(self):
        """ Player chooses to fight the guard """
        current_position = self.current_state['player_position']
        guards_in_room = [guard for guard in self.guards if self.current_state['guard_positions'][guard] == current_position]
        
        if guards_in_room:
            guard = guards_in_room[0]  # Choose one guard to fight
            strength = self.guards[guard]['strength']
            
            # Player tries to fight the guard
            if random.random() > strength:  # Successful fight
                self.move_player_to_random_adjacent()  # Move player to a random adjacent cell after victory
                return f"Fought {guard} and won!", self.rewards['combat_win']
            else:  # Player loses the fight
                if self.current_state['player_health'] == 'Full':
                    self.current_state['player_health'] = 'Injured'
                elif self.current_state['player_health'] == 'Injured':
                    self.current_state['player_health'] = 'Critical'
                return f"Fought {guard} and lost!", self.rewards['combat_loss']
        return "No guard to fight!"
    
    def try_hide(self):
        """ Player attempts to hide from the guard """
        current_position = self.current_state['player_position']
        guards_in_room = [guard for guard in self.guards if self.current_state['guard_positions'][guard] == current_position]
        
        if guards_in_room:
            guard = guards_in_room[0]  # Choose one guard to hide from
            keenness = self.guards[guard]['keenness']
            
            # Player tries to hide
            if random.random() > keenness:  # Successful hide
                self.move_player_to_random_adjacent()  # Move player to a random adjacent cell after successfully hiding
                return f"Successfully hid from {guard}!"
            else:
                return self.try_fight()  # Hide failed, must fight
        return "No guard to hide from!"
    
    def play_turn(self, action):
        """ Take an action and update the state """
        if action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            return self.move_player(action)
        elif action == 'fight':
            return self.try_fight()
        elif action == 'hide':
            return self.try_hide()

    def play_game(self):
        """ Play the game until the player wins or loses """
        while not self.is_terminal():
            print(f"Current state: {self.current_state}")
            action = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT', 'fight', 'hide'])
            print(f"Action: {action}")
            result = self.play_turn(action)
            print(f"Result: {result}")
            print("\n")
            
        if self.is_terminal() == 'goal':
            print(f"You've reached the goal! {self.rewards['goal']} points!")
        else:
            print(f"You've been caught! {self.rewards['combat_loss']} points!")

if __name__ == "__main__":
    game = CastleEscapeMDP()
    game.play_game()
