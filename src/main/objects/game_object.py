import pygame
from main.constants import GRID_SIZE


class GameObject:
    """Base class for all game objects"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.width_cells = width_cells
        self.height_cells = height_cells
        
        self.rect = pygame.Rect(
            grid_x * GRID_SIZE,
            grid_y * GRID_SIZE,
            width_cells * GRID_SIZE,
            height_cells * GRID_SIZE
        )
        self.colour = (255, 255, 255)
    
    def draw(self, surface, camera_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= camera_x
        pygame.draw.rect(surface, self.colour, draw_rect)
    
    def is_visible(self, camera_x, screen_width):
        return (self.rect.x - camera_x < screen_width and 
                self.rect.x - camera_x + self.rect.width > 0)
    
    def update(self):
        pass
    
    def on_player_collision(self, player):
        """Called when player collides with this object"""
        pass


class SolidObject(GameObject):
    """Base class for solid platforms and blocks"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
    
    def on_player_collision(self, player):
        """Handle collision with player"""
        world_rect = pygame.Rect(player.display_x, player.y, player.width, player.height)
        prev_world_rect = pygame.Rect(player.prev_display_x, player.prev_y, player.width, player.height)
        
        if world_rect.colliderect(self.rect):
            # Landing on top
            if prev_world_rect.bottom <= self.rect.top + 5:
                player.y = self.rect.top - player.height
                player.y_vel = 0
                player.on_ground = True
                return False
            # Hit from side or bottom - kill player
            else:
                return True
        return False


class HazardObject(GameObject):
    """Base class for hazards that kill the player"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
    
    def on_player_collision(self, player):
        """Kill player on contact"""
        world_rect = pygame.Rect(player.display_x, player.y, player.width, player.height)
        if world_rect.colliderect(self.rect):
            return True
        return False


class TriggerObject(GameObject):
    """Base class for objects that trigger effects when touched"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.triggered = False
    
    def on_player_collision(self, player):
        """Trigger effect when player touches"""
        world_rect = pygame.Rect(player.display_x, player.y, player.width, player.height)
        if world_rect.colliderect(self.rect) and not self.triggered:
            self.apply_effect(player)
            self.triggered = True
        elif not world_rect.colliderect(self.rect):
            self.triggered = False
        return False
    
    def apply_effect(self, player):
        """Override in subclass"""
        pass


class PortalObject(GameObject):
    """Base class for portals that modify player state"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.activated = False
    
    def on_player_collision(self, player):
        """Apply portal effect once"""
        world_rect = pygame.Rect(player.display_x, player.y, player.width, player.height)
        if world_rect.colliderect(self.rect) and not self.activated:
            self.apply_effect(player)
            self.activated = True
        elif not world_rect.colliderect(self.rect):
            self.activated = False
        return False
    
    def apply_effect(self, player):
        """Override in subclass"""
        pass
