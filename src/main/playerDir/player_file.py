import pygame
from main.controller.keyboard_controls import KeyboardController
from main.constants import GRAVITY, JUMP_STRENGTH, PLAYER_SPEED, PLAYER_COLOR


class CollisionDetection:
    def __init__(self, player):
        self.player = player
    
    def check_floor(self, floor):
        if self.player.rect.colliderect(floor.rect):
            self.player.y = floor.y - self.player.height
            self.player.y_vel = 0
            self.player.on_ground = True
            return True
        return False
    
    def check_objects(self, objects):
        """Check collision with all game objects using polymorphism"""
        for obj in objects:
            if obj.on_player_collision(self.player):
                return True
        return False


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.display_x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = PLAYER_COLOR
        self.speed = PLAYER_SPEED
        self.x_vel = 0
        self.y_vel = 0
        self.jump_strength = JUMP_STRENGTH
        self.gravity = GRAVITY
        self.on_ground = False
        self.is_dead = False
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.prev_display_x = x
        self.prev_y = y
        
        self.controller = KeyboardController()
        self.collision = CollisionDetection(self)
        
        # Store initial state
        self.initial_state = {
            'x': x, 'display_x': x, 'y': y,
            'y_vel': 0, 'speed': PLAYER_SPEED,
            'gravity': GRAVITY, 'jump_strength': JUMP_STRENGTH
        }
    
    def reset(self):
        self.display_x = self.initial_state['display_x']
        self.y = self.initial_state['y']
        self.y_vel = self.initial_state['y_vel']
        self.speed = self.initial_state['speed']
        self.gravity = self.initial_state['gravity']
        self.jump_strength = self.initial_state['jump_strength']
        self.on_ground = False
        self.is_dead = False
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, surface):
        pygame.draw.rect(surface, self.colour, (self.x, self.y, self.width, self.height))
    
    def jump(self):
        if self.controller.is_pressed(pygame.K_SPACE) and self.on_ground:
            self.y_vel = self.jump_strength
            return True
        return False
    
    def apply_gravity(self):
        self.y_vel += self.gravity
        self.y += self.y_vel
        self.rect.y = self.y
    
    def move_forward(self):
        self.display_x += self.speed
        self.rect.x = self.x
    
    def die(self):
        self.is_dead = True
        self.speed = 0
        return self.display_x + self.width // 2, self.y + self.height // 2
    
    def update(self, floor, objects, camera_x):
        if self.is_dead:
            return None
        
        self.controller.update()
        self.prev_display_x = self.display_x
        self.prev_y = self.y
        
        self.apply_gravity()
        self.move_forward()
        
        self.on_ground = False
        self.collision.check_floor(floor)
        
        # Check objects for collision (this also sets on_ground for platforms)
        if self.collision.check_objects(objects):
            return self.die()
        
        # Jump after collision detection so on_ground is properly set
        jumped = self.jump()
        
        return jumped
