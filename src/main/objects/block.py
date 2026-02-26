import pygame
from main.constants import GRID_SIZE, GREEN


class Platform:
    def __init__(self, grid_x, grid_y, width_cells, height_cells):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width_cells = width_cells
        self.height_cells = height_cells
        self.colour = GREEN

        self.rect = pygame.Rect(
            grid_x * GRID_SIZE,
            grid_y * GRID_SIZE,
            width_cells * GRID_SIZE,
            height_cells * GRID_SIZE
        )

    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(surface, self.colour, draw_rect)
    
    def is_visible(self, camera_x, screen_width):
        return (self.rect.x - camera_x < screen_width and 
                self.rect.x - camera_x + self.rect.width > 0)
