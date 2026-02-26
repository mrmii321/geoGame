import pygame


class KeyboardController:
    def __init__(self):
        self.keys = pygame.key.get_pressed()
    
    def update(self):
        self.keys = pygame.key.get_pressed()
    
    def is_pressed(self, key):
        return self.keys[key]
