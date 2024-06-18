import sys
import pygame
from .planet import Planet
from .rocket import Rocket
from .gravity import GravityGroup
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

all_rocket_images = [sprites.ship_1, sprites.ship_2, sprites.ship_3]

# We create a smaller group for gravity so we don't have to loop over all the massless particles
gravity_sprites = GravityGroup()
gravity_sprites.add(Planet((cx-100, cy), mass=100))
gravity_sprites.add(Planet((cx+100, cy), mass=100, image_path=sprites.planet_2))

all_sprites = pygame.sprite.Group(gravity_sprites)
rocket = Rocket((cx, cy - 100), image_path=all_rocket_images[-1], particle_group=all_sprites, mode="wrap")
all_sprites.add(rocket)


# Game loop
def main():
    running = True
    dt = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                current_image = all_rocket_images.pop(0)
                all_rocket_images.append(current_image)
                rocket.set_image(current_image)


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

        all_sprites.update(dt=dt, screen_dimensions=(0, 0, WIDTH, HEIGHT), gravity_sprites=gravity_sprites)

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
