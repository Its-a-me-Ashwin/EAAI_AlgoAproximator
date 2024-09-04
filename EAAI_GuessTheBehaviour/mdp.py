import random

class CastleEscapeMDP:
    def __init__(self):
        # Define the rooms (larger number of rooms)
        self.rooms = ['R' + str(i) for i in range(1, 11)]
        
        # Define health states
        self.health_states = ['Full', 'Injured', 'Critical']
        
        # Define the guards with their strengths (affects combat) and keenness (affects hiding)
        self.guards = {
            'G1': {'strength': 0.8, 'keenness': 0.1},  # Guard 1
            'G2': {'strength': 0.6, 'keenness': 0.3},  # Guard 2
            'G3': {'strength': 0.9, 'keenness': 0.2},  # Guard 3
            'G4': {'strength': 0.7, 'keenness': 0.5},  # Guard 4
            'G5': {'strength': 0.5, 'keenness': 0.4}   # Guard 5
        }
        
        # Set initial state
        self.current_state = {
            'player_room': 'R1',
            'player_health': 'Full',
            'guard_positions': {guard: random.choice(self.rooms[:-1]) for guard in self.guards}  # Guards in random rooms (not the exit)
        }

        # Rewards
        self.rewards = {
            'victory': 100,
            'combat_win': 10,
            'combat_loss': -20,
            'defeat': -100
        }
    
    def reset(self):
        """ Resets the game to the initial state """
        self.current_state = {
            'player_room': 'R1',
            'player_health': 'Full',
            'guard_positions': {guard: random.choice(self.rooms[:-1]) for guard in self.guards}  # Guards in random rooms (not the exit)
        }
    
    def move_guard(self):
        """ Randomly moves the guards to a new room """
        for guard in self.guards:
            self.current_state['guard_positions'][guard] = random.choice(self.rooms[:-1])
    
    def is_terminal(self):
        """ Check if the game has reached a terminal state """
        if self.current_state['player_room'] == 'R10':  # Reaching R10 means victory
            return 'victory'
        if self.current_state['player_health'] == 'Critical' and any(self.current_state['guard_positions'][guard] == self.current_state['player_room'] for guard in self.guards):
            return 'defeat'
        return False
    
    def try_move(self, new_room=None):
        """ Player tries to move to a new room """
        current_room = self.current_state['player_room']
        
        # 90% chance to move to goal if in adjacent rooms (R9 or R8)
        if current_room in ['R8', 'R9'] and random.random() <= 0.9:
            if 'R10' not in self.current_state['guard_positions'].values():
                self.current_state['player_room'] = 'R10'
                self.move_guard()
                return f"Moved to R10 (goal)"
            else:
                return "Guard in R10, can't move!"
        
        # If not in R8 or R9 or 90% move fails, choose a random valid room to move to
        if new_room is None:
            available_moves = [room for room in self.rooms if room != current_room]
            new_room = random.choice(available_moves)
        
        # Check if there's a guard in the new room
        if new_room in self.rooms and new_room != 'R10':
            if any(self.current_state['guard_positions'][guard] == new_room for guard in self.guards):
                return f"Guard in {new_room}, can't move!"
            else:
                self.current_state['player_room'] = new_room
                self.move_guard()
                return f"Moved to {new_room}"
        return "Invalid move"
    
    def try_fight(self):
        """ Player chooses to fight the guard """
        current_room = self.current_state['player_room']
        guards_in_room = [guard for guard in self.guards if self.current_state['guard_positions'][guard] == current_room]
        
        if guards_in_room:
            guard = guards_in_room[0]  # Choose one guard to fight
            strength = self.guards[guard]['strength']
            
            # Player tries to fight the guard
            if random.random() > strength:  # Successful fight
                self.move_guard()  # Move guard away on victory
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
        current_room = self.current_state['player_room']
        guards_in_room = [guard for guard in self.guards if self.current_state['guard_positions'][guard] == current_room]
        
        if guards_in_room:
            guard = guards_in_room[0]  # Choose one guard to hide from
            keenness = self.guards[guard]['keenness']
            
            # Player tries to hide
            if random.random() > keenness:  # Successful hide
                self.move_guard()  # Hide success, guards move
                return f"Successfully hid from {guard}!"
            else:
                return self.try_fight()  # Hide failed, must fight
        return "No guard to hide from!"
    
    def play_turn(self, action):
        """ Take an action and update the state """
        if action == 'move':
            return self.try_move()
        elif action == 'fight':
            return self.try_fight()
        elif action == 'hide':
            return self.try_hide()

    def play_game(self):
        """ Play the game until the player wins or loses """
        while not self.is_terminal():
            print(f"Current state: {self.current_state}")
            action = random.choice(['move', 'fight', 'hide'])
            print(f"Action: {action}")
            result = self.play_turn(action)
            print(f"Result: {result}")
            print("\n")
            
        if self.is_terminal() == 'victory':
            print(f"You've escaped the castle! {self.rewards['victory']} points!")
        else:
            print(f"You've been caught! {self.rewards['defeat']} points!")


if __name__ == "__main__":
    game = CastleEscapeMDP()
    game.play_game()
