import pygame
import json
from main.playerDir.player_file import Player
from main.screenDir.screen_file import Display
from main.objects.floor_terrain import FloorTerrain
from main.objects.block import Platform
from main.objects.particle import ParticleSystem
from main.constants import *


class GameState:
    def __init__(self, display):
        self.display = display
        self.player = Player(50, 50, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.floor = FloorTerrain(0, 550, 1000, 50, BLACK)
        self.platforms = []
        self.particle_system = ParticleSystem()
        self.camera_x = 0
        self.current_level = 0
        self.death_timer = 0
        self.score = 0
        
        self.json_file = r"C:\Users\noahf\Desktop\Development\Python\geoGame\src\main\objects.json"
    
    def load_level(self, level):
        self.platforms.clear()
        self.player.reset()
        self.camera_x = 0
        self.death_timer = 0
        self.current_level = level
        
        try:
            with open(self.json_file) as f:
                data = json.load(f)
                if level < len(data):
                    for plat in data[level]:
                        self.platforms.append(
                            Platform(plat["x"], plat["y"], plat["width"], plat["height"])
                        )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading level: {e}")
    
    def reset_level(self):
        self.load_level(self.current_level)
    
    def update(self):
        if self.death_timer > 0:
            self.death_timer -= 1
            if self.death_timer == 0:
                self.reset_level()
            self.particle_system.update()
            return
        
        self.camera_x = self.player.display_x - self.player.x
        
        result = self.player.update(self.floor, self.platforms, self.camera_x)
        
        # Handle death
        if isinstance(result, tuple):
            x, y = result
            self.particle_system.emit(x, y, RED, 20)
            self.death_timer = 60
        # Handle jump
        elif result:
            self.particle_system.emit(
                self.player.x + self.player.width // 2,
                self.player.y + self.player.height,
                WHITE, 5
            )
        
        self.particle_system.update()
        self.score = int(self.player.display_x / 10)
    
    def draw(self):
        self.display.clear()
        
        self.floor.draw(self.display.surface)
        
        for plat in self.platforms:
            if plat.is_visible(self.camera_x, self.display.width):
                plat.draw(self.display.surface, self.camera_x)
        
        self.player.draw(self.display.surface)
        self.particle_system.draw(self.display.surface, self.camera_x)
        
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        self.display.surface.blit(score_text, (10, 10))
        
        self.display.update()
