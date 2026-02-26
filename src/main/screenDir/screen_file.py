import pygame


class Display:
    def __init__(self, width, height, colour):
        self.surface = pygame.display.set_mode((width, height))
        self.colour = colour
        self.width = width
        self.height = height

    def clear(self):
        self.surface.fill(self.colour)
    
    def update(self):
        pygame.display.flip()
