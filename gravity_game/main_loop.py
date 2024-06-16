import pygame
import sys
from .planet import Planet
from .satellite import Satellite

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbital Mechanics Simulator")
clock = pygame.time.Clock()

# Instance creation
planet = Planet(WIDTH // 2, HEIGHT // 2, 50, BLUE)
satellite = Satellite(WIDTH // 2 + 200, HEIGHT // 2, 10, RED)

# Game loop
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        planet.draw(screen)
        satellite.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
