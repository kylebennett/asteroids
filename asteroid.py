import pygame, random
from logger import log_event
from constants import LINE_WIDTH, ASTEROID_COLOUR, ASTEROID_MIN_RADIUS, ASTEROID_MAX_RADIUS
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, ASTEROID_COLOUR, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, dt):
        
        # always kill the parent asteroid
        self.kill()

        # small asteroids are just destroyed
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        new_angle = random.uniform(20, 50)
        
        new_velocity_1 = self.velocity.rotate(new_angle)
        new_velocity_2 = self.velocity.rotate(-new_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        new_asteroid_1 = Asteroid(self.position[0], self.position[1], new_radius)
        new_asteroid_1.velocity = new_velocity_1 * 1.2
        new_asteroid_1.position += new_asteroid_1.velocity * 3 * dt

        new_asteroid_2 = Asteroid(self.position[0], self.position[1], new_radius)
        new_asteroid_2.velocity = new_velocity_2 * 1.2
        new_asteroid_2.position += new_asteroid_2.velocity * 3 * dt

    def bounce(self, dt, direction):
        log_event("asteroid_bounce")
        new_angle = random.uniform(0, 30)
        if direction > 0:
            new_angle = -new_angle
        self.velocity = -self.velocity.rotate(new_angle)
        self.position += self.velocity * dt

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        
        if other is Asteroid:
            return distance > ASTEROID_MAX_RADIUS and (self.radius + other.radius) > distance
        else:
            return (self.radius + other.radius) > distance