import random
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
        else:
            self.rect.center = self.rect.center + self.velocity * dt



class Rocket(pygame.sprite.Sprite):

    def __init__(
            self, 
            pos=pygame.math.Vector2(0, 0), 
            direction: float = 0, 
            image_path = ship_1,
            particle_group = None,
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

       self.set_image(image_path)

    def set_image(self, image_path):
        self._original_image = pygame.image.load(image_path).convert_alpha()
        self.image = None

    @property
    def heading(self):
        return pygame.math.Vector2(0,1).rotate(self._direction)


    def update(self, *args, dt=0, screen_dimensions=None, **kwargs):
        assert screen_dimensions, "screen_dimensions is required"

        v = self.velocity.length()

        if self.auto_pilot and v > 1e-6:
            aoa = self.velocity.angle_to(self.heading)

            # Only rotate if we have a chance of straightening out
            if v < 0.5 or abs(aoa) <= 180:
                if aoa < -1:
                    self.rotate(2)
                elif aoa > 1:
                    self.rotate(-2)

            angle_fuzziness = max(90 * min(0.5, v), 5)
            if abs(aoa) < angle_fuzziness:
                thrust_vector = self.velocity.normalize() * 0.01

                # heading is a unit vector, so the projection is the dot product 
                # - this gives us the thrust in the direction of the heading
                thrust_dimension = thrust_vector.dot(self.heading) 
                
                # In the low-speed domain we always thrust half of our current speed
                thrust_dimension = min(v/25, thrust_dimension)

                self.fire(thrust=thrust_dimension)

        screen_x_min, screen_y_min, screen_x_max, screen_y_max = screen_dimensions

        if self.pos.y < screen_y_min:
            self.velocity.y = abs(self.velocity.y)
        elif self.pos.y > screen_y_max:
            self.velocity.y = -abs(self.velocity.y)

        if self.pos.x < screen_x_min:
            self.velocity.x = abs(self.velocity.x)
        elif self.pos.x > screen_x_max:
            self.velocity.x = -abs(self.velocity.x)

        self.pos += self.velocity * dt

        if self.image is None:
            self.image = pygame.transform.rotate(self._original_image, -self._direction)
            self.rect = self.image.get_rect()

        self.rect.center = self.pos

    def rotate(self, degrees):
        self._direction += degrees
        self.image = None

    def fire(self, thrust=0.01):
        heading = self.heading
        thrust_vector = -heading * thrust
        nozzle_vector = heading * self.rect.width / 2

        nozzle_position = self.rect.center + nozzle_vector
        if self.particle_group:
            self.particle_group.add(Particle(
                nozzle_position,
                self.velocity - thrust_vector * 3,
            ))

        self.velocity += thrust_vector

    def toggle_auto_pilot(self):
        self.auto_pilot = not self.auto_pilot
        
        

