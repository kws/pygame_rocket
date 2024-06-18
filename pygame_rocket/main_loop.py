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

text_font = pygame.font.Font(None, 24)

def draw_text(surface, text, pos, colour="white"):
    text = text_font.render(text, True, colour)
    surface.blit(text, pos)


cx, cy = WIDTH // 2, HEIGHT // 2


rocket = Rocket((cx, cy - 100), image_path=sprites.ship_2)
planet = Planet(
    pos=pygame.Vector2(cx, cy),
    mass=1e24, 
    radius=20, 
    colour="lawngreen" 
)

all_sprites = pygame.sprite.Group([planet, rocket])
rocket.particle_group = all_sprites

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
            rocket.rotate(-2)
            rocket.auto_pilot = False
        if keys[pygame.K_RIGHT]:
            rocket.rotate(2)
            rocket.auto_pilot = False
        if keys[pygame.K_SPACE]:
            rocket.fire()
            rocket.auto_pilot = False
        if keys[pygame.K_h]:
            rocket.auto_pilot = True

        if keys[pygame.K_q]:
            running = False

        all_sprites.update(dt=dt, screen_dimensions=(0, 0, WIDTH, HEIGHT))

        screen.fill((0,0,0))
        all_sprites.draw(screen) 
        draw_text(screen, f"Velocity: {rocket.velocity.magnitude()*1_000:.0f}", (10, 10))
        draw_text(screen, f"Heading: {rocket._direction%360:.0f}", (10, 30))
        if rocket.auto_pilot:
            draw_text(screen, "Auto Pilot", (700, 10), "red")

        pygame.display.flip()
        dt = clock.tick(FPS)

    pygame.quit()
    sys.exit()
