import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Game constants
WIDTH = 400
HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
SKY_BLUE = (135, 206, 235)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# Game variables
score = 0
high_score = 0
game_active = False
font = pygame.font.SysFont('Arial', 30)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.radius = 15
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Check if bird hits the ground or ceiling
        if self.y >= HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            return False
        elif self.y <= self.radius:
            self.y = self.radius
            return True
        return True
        
    def draw(self):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, int(self.y)), self.radius)
        # Draw eye
        pygame.draw.circle(screen, BLACK, (self.x + 5, int(self.y) - 3), 3)
        # Draw beak
        pygame.draw.polygon(screen, (255, 165, 0), 
                          [(self.x + 15, int(self.y)), 
                           (self.x + 25, int(self.y) - 3), 
                           (self.x + 25, int(self.y) + 3)])

class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.top_height = random.randint(50, HEIGHT - 200)
        self.bottom_height = HEIGHT - self.top_height - PIPE_GAP
        self.width = 60
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, HEIGHT - self.bottom_height, self.width, self.bottom_height))
        
    def collide(self, bird):
        # Check collision with top pipe
        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width and 
            bird.y - bird.radius < self.top_height):
            return True
        # Check collision with bottom pipe
        if (bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width and 
            bird.y + bird.radius > HEIGHT - self.bottom_height):
            return True
        return False

def draw_score():
    score_surface = font.render(f'Score: {score}', True, BLACK)
    screen.blit(score_surface, (10, 10))
    
    high_score_surface = font.render(f'High Score: {high_score}', True, BLACK)
    screen.blit(high_score_surface, (10, 50))

def draw_game_over():
    game_over_surface = font.render('Game Over! Press SPACE to restart', True, BLACK)
    screen.blit(game_over_surface, (WIDTH//2 - 180, HEIGHT//2))

def main():
    global score, high_score, game_active
    
    bird = Bird()
    pipes = []
    last_pipe = pygame.time.get_ticks()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    bird.flap()
                if event.key == pygame.K_SPACE and not game_active:
                    game_active = True
                    bird = Bird()
                    pipes = []
                    score = 0
                    last_pipe = pygame.time.get_ticks()
        
        # Clear screen
        screen.fill(SKY_BLUE)
        
        if game_active:
            # Bird update
            game_active = bird.update()
            
            # Pipe generation
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > PIPE_FREQUENCY:
                pipes.append(Pipe())
                last_pipe = time_now
                
            # Pipe update and collision detection
            for pipe in pipes[:]:
                pipe.update()
                
                # Check if bird passed the pipe
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                    if score > high_score:
                        high_score = score
                
                # Check collision
                if pipe.collide(bird):
                    game_active = False
                
                # Remove pipes that are off screen
                if pipe.x < -pipe.width:
                    pipes.remove(pipe)
            
            # Draw pipes
            for pipe in pipes:
                pipe.draw()
            
            # Draw bird
            bird.draw()
            
            # Draw score
            draw_score()
        else:
            draw_game_over()
            draw_score()
        
        # Update display
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()