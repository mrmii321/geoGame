import pygame
from main.main_collector import Main
from main.controller.keyboard_controls import KeyboardController
from main.mainMenu.main_menu import MenuSystem
from main.constants import MENU, LEVEL_SELECT, PLAYING, FPS

pygame.init()


class App:
    def __init__(self):
        self.running = True
        self.controller = KeyboardController()
        self.main = Main()
        self.menu_system = MenuSystem(self.main.display)
        self.state = MENU
        self.clock = pygame.time.Clock()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.clock.tick(FPS)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state in (MENU, LEVEL_SELECT):
                selected_level = self.menu_system.handle_event(event)
                if selected_level is not None:
                    self.main.load_level(selected_level)
                    self.state = PLAYING
            
            elif self.state == PLAYING:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = MENU
                    self.menu_system.state = MENU
        
        self.controller.update()
        
        if self.state in (MENU, LEVEL_SELECT):
            self.menu_system.update()
        elif self.state == PLAYING:
            self.main.update()


if __name__ == "__main__":
    App().run()
