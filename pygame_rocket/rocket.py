import random
from typing import Literal
import pygame
from .sprites import ship_1

class Particle(pygame.sprite.Sprite):
    def __init__(
            self,
            pos,
            velocity,
    ):
        super().__init__()

        self.velocity = velocity
        self.color = pygame.Color("red")

        self.image = pygame.Surface([3, 3], pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 255))
        pygame.draw.circle(self.image, "red", (1, 1), 3, 2)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.age = 0
        self.life_span = 1_000 + random.randint(-500, 500)

    def update(self, *args, dt=0, **kwargs):
        self.age += dt
        if self.age > self.life_span:
            self.kill()
            return
        
        self.rect.center = self.rect.center + self.velocity * dt
        h, s, v, a = self.color.hsva
        h += random.randrange(-10, 10)
        self.color.hsva = (h % 360, s, v, a)
        self.image.fill((0, 0, 0, 255))
        pygame.draw.circle(self.image, self.color, (1, 1), 3, 2)




class Rocket(pygame.sprite.Sprite):

    def __init__(
            self, 
            pos=pygame.math.Vector2(0, 0), 
            direction: float = 0, 
            image_path = ship_1,
            particle_group = None,
            mode: Literal["bounce", "wrap", "infinite"] = "bounce"
        ):
       
       # Call the parent class (Sprite) constructor
       super().__init__()

       # Make sure objects are of the right type
       self.pos = pygame.math.Vector2(pos)
       self.velocity = pygame.math.Vector2(0, 0)
       self._direction = float(direction)
       self.image = None
       self.particle_group = particle_group
       self.auto_pilot = False
       self.mode = mode

       self.set_image(image_path)

    def set_image(self, image_path):
        self._original_image = pygame.image.load(image_path).convert_alpha()
        self.image = None

    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, value):
        self._direction = value
        self.image = None

    @property
    def heading(self):
        return pygame.math.Vector2(0,1).rotate(self._direction)


    def update(self, *args, dt=0, screen_dimensions=None, gravity_sprites=None, **kwargs):
        assert screen_dimensions, "screen_dimensions is required"

        # Bounce off the walls
        if self.mode == "bounce":
            self.check_bounce(screen_dimensions)
        elif self.mode == "wrap":
            self.check_wrap(screen_dimensions)

        # Add a velocity component from gravity
        if gravity_sprites:
            for x, y, mass in gravity_sprites.all_com:
                gravity_vector = pygame.math.Vector2(x, y) - self.pos
                gravity_vector = gravity_vector.normalize() * mass / gravity_vector.length_squared()
                gravity_vector = gravity_vector * dt * 0.01
                if gravity_vector.length() > 1:
                    gravity_vector = gravity_vector.normalize()
                self.velocity += gravity_vector

        if self.auto_pilot:
            self.auto_pilot_update()

        self.pos += self.velocity * dt

        if self.image is None:
            self.image = pygame.transform.rotate(self._original_image, -self._direction)
            self.rect = self.image.get_rect()

        self.rect.center = self.pos

    def check_bounce(self, screen_dimensions):
        screen_x_min, screen_y_min, screen_x_max, screen_y_max = screen_dimensions

        if self.pos.y < screen_y_min:
            self.pos.y = screen_y_min
            self.velocity.y = abs(self.velocity.y)
        elif self.pos.y > screen_y_max:
            self.pos.y = screen_y_max
            self.velocity.y = -abs(self.velocity.y)
            
        if self.pos.x < screen_x_min:
            self.pos.x = screen_x_min
            self.velocity.x = abs(self.velocity.x)
        elif self.pos.x > screen_x_max:
            self.pos.x = screen_x_max
            self.velocity.x = -abs(self.velocity.x)

    def check_wrap(self, screen_dimensions):
        screen_x_min, screen_y_min, screen_x_max, screen_y_max = screen_dimensions

        if self.pos.y < screen_y_min:
            self.pos.y = screen_y_max
        elif self.pos.y > screen_y_max:
            self.pos.y = screen_y_min
            
        if self.pos.x < screen_x_min:
            self.pos.x = screen_x_max
        elif self.pos.x > screen_x_max:
            self.pos.x = screen_x_min

    def auto_pilot_update(self):
        """
        The autopilot will attempt to keep the rocket stationary. 

        It will rotate the rocket to face the direction of travel, and then thrust in that direction.

        If the rocket is moving too fast so it won't have time to turn before hitting the edge of the screen,
        it will not rotate and instead wait for a more favourable time.
        """
        v = self.velocity.length()

        if v > 1e-6: # Only run if enabled and we're moving
            aoa = self.velocity.angle_to(self.heading) % 360

            # Only rotate if we have a chance of straightening out
            if self.mode == "wrap" or (v < 0.5 or abs(aoa) <= 180):
                if aoa < 180:
                    self.rotate(-2)
                else:
                    self.rotate(2)

            if aoa < 45 or aoa > 315:
                thrust_vector = self.velocity.normalize() * 0.01

                # heading is a unit vector, so the projection is the dot product 
                # - this gives us the thrust in the direction of the heading
                thrust_dimension = thrust_vector.dot(self.heading) 
                
                # In the low-speed domain we always thrust half of our current speed
                thrust_dimension = min(v/25, thrust_dimension)

                self.fire(thrust=thrust_dimension)

    def rotate(self, degrees):
        self._direction += degrees
        self.image = None

    def fire(self, thrust=0.01):
        heading = self.heading
        thrust_vector = -heading * thrust
        nozzle_vector = heading * self.rect.width * 0.65

        if self.particle_group:
            for _ in range(25):
                if random.random() > thrust*100 :
                    continue

                nozzle_position = pygame.math.Vector2(self.rect.center)
                nozzle_position.x += random.randint(-3, 3)
                nozzle_position += nozzle_vector

                rotation = random.random() * 20 - 10   
                particle_heading = heading.rotate(rotation)
                particle_velocity = particle_heading * (0.1 + random.random() * 0.2)

                self.particle_group.add(Particle(
                    nozzle_position,
                    self.velocity + particle_velocity
                ))

        self.velocity += thrust_vector

    def toggle_auto_pilot(self):
        self.auto_pilot = not self.auto_pilot
        
        

