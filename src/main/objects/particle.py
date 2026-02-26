import pygame
import random


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.color = color
        self.lifetime = 30
        self.size = random.randint(2, 5)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.lifetime -= 1
    
    def draw(self, surface, camera_x):
        if self.lifetime > 0:
            alpha = int(255 * (self.lifetime / 30))
            color_with_alpha = (*self.color[:3], alpha)
            pygame.draw.circle(surface, self.color, (int(self.x - camera_x), int(self.y)), self.size)
    
    def is_alive(self):
        return self.lifetime > 0


class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color, count=10):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def draw(self, surface, camera_x):
        for particle in self.particles:
            particle.draw(surface, camera_x)
