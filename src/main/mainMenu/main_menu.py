import pygame
from main.constants import *


class MenuSystem:
    def __init__(self, display):
        self.display = display
        self.selected_level = 0
        self.max_levels = 4
        self.state = MENU
        
    def handle_event(self, event):
        if self.state == MENU:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = LEVEL_SELECT
        
        elif self.state == LEVEL_SELECT:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_level = (self.selected_level - 1) % self.max_levels
                elif event.key == pygame.K_DOWN:
                    self.selected_level = (self.selected_level + 1) % self.max_levels
                elif event.key == pygame.K_RETURN:
                    return self.selected_level
                elif event.key == pygame.K_ESCAPE:
                    self.state = MENU
        return None
    
    def update(self):
        if self.state == MENU:
            self._draw_main_menu()
        elif self.state == LEVEL_SELECT:
            self._draw_level_select()
        
    def _draw_main_menu(self):
        self.display.surface.fill(DARK_BLUE)
        
        title_font = pygame.font.Font(None, 80)
        subtitle_font = pygame.font.Font(None, 40)
        
        title = title_font.render("GEO GAME", True, BLUE)
        subtitle = subtitle_font.render("Press ENTER to Start", True, WHITE)
        
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 350))
        
        self.display.surface.blit(title, title_rect)
        self.display.surface.blit(subtitle, subtitle_rect)
        
        pygame.display.flip()
    
    def _draw_level_select(self):
        self.display.surface.fill((30, 20, 50))
        
        title_font = pygame.font.Font(None, 60)
        level_font = pygame.font.Font(None, 40)
        
        title = title_font.render("SELECT LEVEL", True, PURPLE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.display.surface.blit(title, title_rect)
        
        for i in range(self.max_levels):
            color = (255, 200, 100) if i == self.selected_level else GRAY
            level_text = level_font.render(f"Level {i + 1}", True, color)
            level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 60))
            
            if i == self.selected_level:
                pygame.draw.rect(self.display.surface, (80, 50, 120), level_rect.inflate(20, 10), 3, 5)
            
            self.display.surface.blit(level_text, level_rect)
        
        hint = pygame.font.Font(None, 30).render("UP/DOWN: Navigate | ENTER: Select | ESC: Back", True, (100, 100, 100))
        self.display.surface.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, 520)))
        
        pygame.display.flip()
