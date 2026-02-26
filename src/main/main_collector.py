from main.game_state import GameState
from main.screenDir.screen_file import Display
from main.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE


class Main:
    def __init__(self):
        self.display = Display(SCREEN_WIDTH, SCREEN_HEIGHT, WHITE)
        self.game_state = GameState(self.display)
    
    def load_level(self, level):
        self.game_state.load_level(level)
    
    def update(self):
        self.game_state.update()
        self.game_state.draw()
