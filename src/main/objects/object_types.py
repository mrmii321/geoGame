import pygame
from main.objects.game_object import SolidObject, HazardObject, TriggerObject, PortalObject
from main.constants import GREEN, RED, PURPLE, BLUE, GRAY


class Block(SolidObject):
    """Standard platform block"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = GREEN


class Spike(HazardObject):
    """Spike that kills player on contact"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = RED


class JumpPad(TriggerObject):
    """Pad that launches player upward"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = PURPLE
        self.jump_power = -15
    
    def apply_effect(self, player):
        player.y_vel = self.jump_power


class JumpOrb(TriggerObject):
    """Orb that gives player a jump when clicked"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 255, 0)
        self.jump_power = -12
    
    def apply_effect(self, player):
        if player.controller.is_pressed(pygame.K_SPACE):
            player.y_vel = self.jump_power


class GravityPortal(PortalObject):
    """Portal that flips gravity"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = BLUE
    
    def apply_effect(self, player):
        player.gravity *= -1
        player.jump_strength *= -1


class SpeedPortal(PortalObject):
    """Portal that changes player speed"""
    def __init__(self, grid_x, grid_y, width_cells=1, height_cells=1, speed_multiplier=2.0):
        super().__init__(grid_x, grid_y, width_cells, height_cells)
        self.colour = (255, 165, 0)
        self.speed_multiplier = speed_multiplier
    
    def apply_effect(self, player):
        player.speed = player.initial_state['speed'] * self.speed_multiplier
