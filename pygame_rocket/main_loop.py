import sys
import pygame
from .planet import Planet
from .rocket import Rocket
from . import sprites

WIDTH = 800
HEIGHT = 600
FPS = 60

# Initialization
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rocket Simulator")
clock = pygame.time.Clock()

text_font = pygame.font.Font(None, 12)  

cx, cy = WIDTH // 2, HEIGHT // 2


rocket = Rocket((cx, cy - 100), image_path=sprites.ship_2)
planet = Planet(
    pos=pygame.Vector2(cx, cy),
    mass=1e24, 
    radius=20, 
    colour="lawngreen" 
)

all_sprites = pygame.sprite.Group([planet, rocket])

# Game loop
def main():
    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            rocket.rotate(2)
        if keys[pygame.K_RIGHT]:
            rocket.rotate(-2)
        if keys[pygame.K_SPACE]:
            rocket.fire()

        if keys[pygame.K_q]:
            running = False

        all_sprites.update(dt=dt, screen_dimensions=(0, 0, WIDTH, HEIGHT))

        screen.fill((0,0,0))
        all_sprites.draw(screen) 

        pygame.display.flip()
        dt = clock.tick(FPS)

    pygame.quit()
    sys.exit()
