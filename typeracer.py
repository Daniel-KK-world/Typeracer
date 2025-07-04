import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
TRACK_HEIGHT = 300
LANE_WIDTH = 200
PLAYER_X = 100
AI_X = 100
FONT_SIZE = 24
BG_COLOR = (50, 50, 80)
TRACK_COLOR = (30, 30, 50)
CAR_WIDTH, CAR_HEIGHT = 60, 30  # These will be updated based on the actual image size

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", FONT_SIZE)
font_large = pygame.font.SysFont("Arial", 36)

# Word list (adjust difficulty)
word_list = ["speed", "race", "typing", "keyboard", "python", "code", "fast", "win", "car", "lap"]


class Car:
    def __init__(self, x, y, is_player=True):
        self.x = x
        self.y = y
        self.is_player = is_player
        
        # Load car image
        if is_player:
            self.image = pygame.image.load("car1.png").convert_alpha()
        else:
            self.image = pygame.image.load("car2.png").convert_alpha()
            
        # Scale the image if needed (optional)
        self.image = pygame.transform.scale(self.image, (CAR_WIDTH, CAR_HEIGHT))
        
        # Get the actual dimensions from the image
        self.rect = self.image.get_rect()
        self.width = self.rect.width
        self.height = self.rect.height
        
        self.speed = 0
        self.max_speed = 5
        self.current_word = ""
        self.typed_so_far = ""

    def draw(self, screen):
        # Draw the car image
        screen.blit(self.image, (self.x, self.y))
        
        # Draw word above car
        word_text = font.render(self.current_word, True, WHITE)
        screen.blit(word_text, (self.x, self.y - 30))

        # Draw typed progress
        typed_text = font.render(self.typed_so_far, True, GREEN)
        screen.blit(typed_text, (self.x, self.y - 60))

    def update(self):
        self.x += self.speed
        # Slow down over time (drag)
        self.speed *= 0.95

    def assign_new_word(self):
        self.current_word = random.choice(word_list)
        self.typed_so_far = ""

class Game:
    def __init__(self):
        self.player = Car(PLAYER_X, 150, True)  # Player car
        self.ai = Car(AI_X, 250, False)        # AI car
        self.player.assign_new_word()
        self.ai.assign_new_word()
        self.game_over = False
        self.winner = None
        self.clock = pygame.time.Clock()
        self.ai_speed = 0.5  # AI base speed (adjust difficulty)

    def update_ai(self):
        # Simulate AI typing (random speed)
        if random.random() < 0.02:  # 2% chance per frame to type a letter
            self.ai.typed_so_far += self.ai.current_word[len(self.ai.typed_so_far)]
        
        # If AI completes word, move forward
        if self.ai.typed_so_far == self.ai.current_word:
            self.ai.speed += self.ai_speed
            self.ai.assign_new_word()
            
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Typing Race Game")
    game = Game()
    current_input = ""

    running = True
    while running:
        screen.fill(BG_COLOR)

        # Draw racetrack
        pygame.draw.rect(screen, TRACK_COLOR, (0, 100, WIDTH, TRACK_HEIGHT))
        pygame.draw.line(screen, WHITE, (0, 200), (WIDTH, 200), 2)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                else:
                    current_input += event.unicode.lower()

        # Check if player typed the word
        if current_input.lower() == game.player.current_word:
            game.player.speed += 2  # Boost speed
            game.player.assign_new_word()
            current_input = ""

        # Track player typing progress
        game.player.typed_so_far = ""
        for i in range(min(len(current_input), len(game.player.current_word))):
            if current_input[i] == game.player.current_word[i]:
                game.player.typed_so_far += current_input[i]

        # Update AI
        game.update_ai()

        # Update cars
        game.player.update()
        game.ai.update()

        # Check race finish
        if game.player.x >= WIDTH - game.player.width:
            game.game_over = True
            game.winner = "PLAYER"
        elif game.ai.x >= WIDTH - game.ai.width:
            game.game_over = True
            game.winner = "AI"

        # Draw cars
        game.player.draw(screen)
        game.ai.draw(screen)

        # Draw UI
        input_text = font.render(f"Typing: {current_input}", True, WHITE)
        screen.blit(input_text, (20, HEIGHT - 50))

        # Game over screen
        if game.game_over:
            result_text = font_large.render(f"{game.winner} WINS!", True, YELLOW)
            screen.blit(result_text, (WIDTH // 2 - 100, HEIGHT // 2))
            restart_text = font.render("Press SPACE to restart", True, WHITE)
            screen.blit(restart_text, (WIDTH // 2 - 100, HEIGHT // 2 + 50))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            game = Game()  # Reset game
                            current_input = ""
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            waiting = False
                            running = False

        pygame.display.flip()
        game.clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()