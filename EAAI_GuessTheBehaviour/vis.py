import pygame
import sys
import random
from mdp import CastleEscapeMDP  # Import the CastleEscapeMDP class

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 600  # Enough to fit all 10 rooms
GRID_SIZE = 5  # 5 columns and 2 rows
CELL_WIDTH = WIDTH // GRID_SIZE
CELL_HEIGHT = HEIGHT // 2

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)  # Color for the goal room

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Castle Escape MDP Visualization")

# Initialize MDP game
game = CastleEscapeMDP()

# Map room to grid cell positions
def room_to_grid(room):
    room_index = int(room[1:]) - 1  # Room numbers are 'R1', 'R2', ..., 'R10'
    col = room_index % GRID_SIZE
    row = room_index // GRID_SIZE
    return col * CELL_WIDTH, row * CELL_HEIGHT

# Draw the grid for the rooms
def draw_grid():
    for x in range(0, WIDTH, CELL_WIDTH):
        for y in range(0, HEIGHT, CELL_HEIGHT):
            rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Draw the goal room (R10) in yellow
def draw_goal_room():
    x, y = room_to_grid('R10')
    rect = pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)
    pygame.draw.rect(screen, YELLOW, rect)
    font = pygame.font.Font(None, 36)
    label = font.render('Goal', True, BLACK)
    screen.blit(label, (x + CELL_WIDTH // 4, y + CELL_HEIGHT // 4))

# Draw player at a given position
def draw_player(room):
    x, y = room_to_grid(room)
    center_x = x + CELL_WIDTH // 3
    center_y = y + CELL_HEIGHT // 2
    pygame.draw.circle(screen, GREEN, (center_x, center_y), CELL_WIDTH // 6)

# Draw guards at their positions
def draw_guards(guard_positions):
    for guard, position in guard_positions.items():
        x, y = room_to_grid(position)
        rect = pygame.Rect(x + 2 * CELL_WIDTH // 3 - 10, y + CELL_HEIGHT // 3, CELL_WIDTH // 4, CELL_HEIGHT // 3)
        pygame.draw.rect(screen, RED, rect)
        # Label the guard
        font = pygame.font.Font(None, 24)
        label = font.render(guard, True, WHITE)
        screen.blit(label, (x + 2 * CELL_WIDTH // 3, y + CELL_HEIGHT // 3))

# Draw player and guard together if they are in the same room
def draw_player_and_guard_together(room, guard_positions):
    guards_in_room = [guard for guard, pos in guard_positions.items() if pos == room]
    if guards_in_room:
        # Draw the player on the left and guard on the right
        x, y = room_to_grid(room)
        center_x = x + CELL_WIDTH // 4
        center_y = y + CELL_HEIGHT // 2
        pygame.draw.circle(screen, GREEN, (center_x, center_y), CELL_WIDTH // 6)
        
        guard_x = x + 3 * CELL_WIDTH // 4
        pygame.draw.rect(screen, RED, (guard_x - CELL_WIDTH // 6, center_y - CELL_HEIGHT // 6, CELL_WIDTH // 3, CELL_HEIGHT // 3))
        
        # Label the guard
        font = pygame.font.Font(None, 24)
        label = font.render(guards_in_room[0], True, WHITE)
        screen.blit(label, (guard_x - 10, center_y - 10))

# Draw player health status
def draw_health(health):
    font = pygame.font.Font(None, 36)
    health_text = f"Health: {health}"
    health_surface = font.render(health_text, True, BLUE)
    screen.blit(health_surface, (10, HEIGHT - 50))

# Display victory or defeat message
def display_end_message(message):
    font = pygame.font.Font(None, 100)
    text_surface = font.render(message, True, DARK_GRAY)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True
    action_results = []
    game_ended = False
    end_message = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_ended:
                    # Play one turn in the game when the spacebar is pressed
                    action = random.choice(['move', 'fight', 'hide'])
                    result = game.play_turn(action)
                    action_results.append(f"Action: {action}, Result: {result}")

        screen.fill(WHITE)
        draw_grid()

        # Draw the goal room (R10) in yellow
        draw_goal_room()

        # Check if player and a guard are in the same room and draw them together
        if game.current_state['player_room'] in game.current_state['guard_positions'].values():
            draw_player_and_guard_together(game.current_state['player_room'], game.current_state['guard_positions'])
        else:
            # Draw the player and guards in separate positions
            draw_player(game.current_state['player_room'])
            draw_guards(game.current_state['guard_positions'])

        # Display player health
        draw_health(game.current_state['player_health'])

        # Check for terminal state
        if game.is_terminal() == 'victory':
            game_ended = True
            end_message = "Victory!"
        elif game.is_terminal() == 'defeat':
            game_ended = True
            end_message = "Defeat!"

        if game_ended:
            display_end_message(end_message)

        # Print the latest 5 results on the screen
        font = pygame.font.Font(None, 24)
        y_offset = 10
        for result in action_results[-5:]:
            result_surface = font.render(result, True, BLACK)
            screen.blit(result_surface, (10, y_offset))
            y_offset += 30

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
